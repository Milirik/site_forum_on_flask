from app import app, db
from flask import render_template, request, redirect, url_for, session
from forms import Forms1
from models import Post, User, Answer
from check_log_in import check_logged_in, forbid_transition_if_logged_in
from threading import Thread
import datetime
# from flask_security import datastore, login_required

@app.route("/")
def main_page()->'html':
    posts = Post.query.all()
    return render_template('main.html', posts=posts)

@app.route("/profile")
@check_logged_in
def profile_page()->'html':
    f = Forms1()
    us = User.query.filter(User.nick == session['nick']).first()
    return render_template('profile.html', form=f, posts=us.posts_)

@app.route("/<post_id>/discuss", methods=['GET', 'POST'])
def discuss_page(post_id)->'html':
    post = Post.query.filter(Post.id==post_id).first_or_404()
    return render_template('discuss.html', post=post)

@app.route("/create_new_post", methods=['GET', 'POST'])
@check_logged_in
def create_new_post_page()->'html':
    f = Forms1()
    if request.method == 'POST':
        us = User.query.filter(User.nick == session['nick']).first()
        if (us.k_posts < 3) and ((datetime.datetime.now() - us.date_block).seconds > 60):
            title = request.form['name']
            body = request.form['text']
            new_post = Post(title=title, body=body)
            db.session.add(new_post)
            us.posts_.append(new_post)
            us.k_posts += 1
            db.session.commit()
            return redirect(url_for('main_page'))
        else:
            us.date_block = datetime.datetime.now()
            us.k_posts = 0
            db.session.commit()
            return redirect(url_for('block_page'))
    else:
        return render_template('create_new_post.html', form=f)

@app.route("/<post_id>/discuss/create_new_answer", methods=['GET', 'POST'])
@check_logged_in
def create_new_answer_page(post_id) -> 'html':
    f = Forms1()
    if request.method == 'POST':
        us = User.query.filter(User.nick == session['nick']).first()
        if (us.k_answers < 5) and ((datetime.datetime.now() - us.date_block).seconds > 60):
            current_post = Post.query.filter(Post.id == post_id).first()
            body = request.form['text']
            new_answer = Answer(body=body)
            db.session.add(new_answer)
            us.answers_.append(new_answer)
            current_post.answers_.append(new_answer)
            us.k_answers += 1
            db.session.commit()
            return redirect(url_for('discuss_page', post_id=post_id))
        else:
            us.date_block = datetime.datetime.now()
            us.k_answers = 0
            return redirect(url_for('block_page'))
    else:
        return render_template('answer.html', form=f, post_id=post_id)

@app.route("/registration", methods=["GET", "POST"])
@forbid_transition_if_logged_in
def registration_page() ->'html':
    f = Forms1()
    if request.method == 'POST':
        users = [i.nick for i in User.query.all()]
        emails = [i.email for i in User.query.all()]
        if (request.form['nick'] not in users) and (request.form['email'] not in emails) and request.form['nick'] and request.form['password']:
            new_user = User(nick=request.form['nick'],
                            email=request.form['email'],
                            password=request.form['password'],
                            k_answers=0,
                            k_posts=0,
                            date_block=datetime.datetime(2017, 1, 1, 1, 1, 1),
                            active=False)
            db.session.add(new_user)
            db.session.commit()
            print('Registr')
            return redirect(url_for('login_page'))
        else:
            return render_template('registr.html', form=f)
    else:
        return render_template('registr.html', form=f)

@app.route("/login", methods=['GET', 'POST'])
@forbid_transition_if_logged_in
def login_page() ->'html':
    f = Forms1()
    if request.method == 'GET':
        return render_template('login.html', form=f)
    else:
        us = User.query.filter(User.nick==request.form['nick']).first()
        if us:
            if us.password==request.form['password']:
                session['logged_in'] = True
                session['nick'] = us.nick
                us.active = True
                db.session.commit()
                return redirect(url_for('main_page'))
            else:
                return render_template('login.html', form=f, incorrect='f_pas')
        return render_template('login.html', form=f, incorrect='f_us')

@app.route("/logout")
def logout() -> 'html':
    try:
        us = User.query.filter(User.nick == session['nick']).first()
        session.pop('logged_in')
        session.pop('nick')
        us.k_posts = 0
        us.k_answers = 0
        us.active = False
        db.session.commit()
        return redirect(url_for('main_page'))
    except:
        return 404

@app.route("/<for_profile>")
@check_logged_in
def for_profile_page(for_profile) -> 'html':
    if for_profile == session['nick']:
        return redirect(url_for('profile_page'))
    else:
        us = User.query.filter(User.nick == for_profile).first()
        if us:
            return render_template('foreign_profile.html', f_p=for_profile, posts=us.posts_)
        return render_template('foreign_profile.html', f_p=for_profile, posts=[])


@app.route("/block")
def block_page() -> 'html':
    return render_template('block.html')

@app.route("/admin")
def admin() -> 'html':
    return render_template('block.html')

@app.errorhandler(404)
def page_not_found(e) -> 'html':
    return render_template('error404.html'), 404
