from wtforms import Form, StringField, TextAreaField, PasswordField, FileField
from wtforms.validators import EqualTo, Email, DataRequired, Length

class Forms1(Form):
    name = StringField(validators=[Length(max=10)])
    text = TextAreaField(validators=[Length(max=10)])
    password = PasswordField()
    password1 = PasswordField()
    nick = StringField()
    nick1 = StringField()
    email = StringField()
    picture = FileField()
