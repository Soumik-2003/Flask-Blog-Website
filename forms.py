from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL, Length, Email, EqualTo
from flask_ckeditor import CKEditorField




class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


class RegisterForm(FlaskForm):
    full_name = StringField('Full Name', validators=[
        DataRequired(),
        Length(max=250)
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email(),
        Length(max=250)
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(max=250)
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        Length(max=250),
        EqualTo('password', message='Passwords must match.')
    ])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(),
        Email(),
        Length(max=250)
    ])

    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(max=250)
    ])
    submit = SubmitField('Login')

class Comment(FlaskForm):
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField('Submit Comment')