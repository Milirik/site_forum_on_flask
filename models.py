from app import db
from datetime import datetime
# from flask_security import UserMixin, RoleMixin

users_posts = db.Table('users_posts',
                       db.Column('users_id', db.Integer, db.ForeignKey('users.id')),
                       db.Column('posts_id', db.Integer, db.ForeignKey('posts.id')))
posts_answers = db.Table('posts_answers',
                         db.Column('posts_id', db.Integer, db.ForeignKey('posts.id')),
                         db.Column('answers_id', db.Integer, db.ForeignKey('answers.id')))
users_answers = db.Table('users_answers',
                         db.Column('answers_id', db.Integer, db.ForeignKey('answers.id')),
                         db.Column('users_id', db.Integer, db.ForeignKey('users.id')))

# roles_users = db.Table("roles_users",
#                        db.Column('roles_id', db.Integer, db.ForeignKey('roles.id')),
#                        db.Column('users_id', db.Integer, db.ForeignKey('users.id')))

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    body = db.Column(db.Text)
    created_time = db.Column(db.DateTime, default=datetime.now())
    answers_ = db.relationship('Answer', secondary=posts_answers, backref=db.backref('posts1'))

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Post id: {}, title: {}>'.format(self.id, self.title)


class Answer(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    created_time = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, *args, **kwargs):
        super(Answer, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Answer id: {}, body: {}>'.format(self.id, self.body)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    # Для ограничения постов и ответов
    date_block = db.Column(db.DateTime)
    k_answers = db.Column(db.Integer)
    k_posts =db.Column(db.Integer)
    nick = db.Column(db.String(140), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    email = db.Column(db.String(140), unique=True)
    image = db.Column(db.LargeBinary, nullable=True)
    posts_ = db.relationship('Post', secondary=users_posts, backref=db.backref('users1'))
    answers_ = db.relationship('Answer', secondary=users_answers, backref=db.backref('users2'))
    # roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users3'))

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    def __repr__(self):
      return '<User id: {}, User nick: {}>'.format(self.id, self.nick)

# class Role(db.Model):
#     __tablename__ = 'roles'
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(100), unique=True)