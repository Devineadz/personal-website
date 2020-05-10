from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, SelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Email, Length, DataRequired


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    email = EmailField('Email', validators=[InputRequired(), Email()])
    message = TextAreaField('Message', validators=[InputRequired()], render_kw={'rows': 10})
    send = SubmitField('Send')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class BlogForm(FlaskForm):
    blog_title = StringField('Title', validators=[InputRequired()])
    content = TextAreaField('Content', validators=[InputRequired()], render_kw={'rows': 10})
    topic_area = SelectField('Drop down select topic area', validators=[InputRequired()],
                             choices=[('Web development', 'Web development'), ('Game Development', 'Game development'),
                                      ('Other development', 'Other development'), ('Other', 'Other')])
    submit = SubmitField('Submit')