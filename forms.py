from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    first_name = StringField('First name',
    validators=[DataRequired(message="please, enter your first name"),
    Length(min=2, max=20,
    message="first name must be at leat 2 characters and maximum 20 characters")])

    last_name = StringField('Last name',
    validators=[DataRequired(message="please, enter your last name"),
    Length(min=2, max=20,
    message="last name must be at leat 2 characters and maximum 20 characters")])

    email = StringField('Email',
    validators=[DataRequired(message="please, enter your email"),
    Email(message="enter a valid email")])

    password = PasswordField('Password',
    validators=[DataRequired(message="please, enter your password"),
    Length(min=6, max=40,
    message="password must be at leat 6 characters and maximum 40 characters")])

    confirm_password = PasswordField('Confirm Password',
    validators=[DataRequired(message="please, confirm your password"),
    EqualTo('password', message="password doesn't match")])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(message="please, enter your email"),
                        Email(message="enter a valid email")])
    password = PasswordField('Password',
    validators=[DataRequired(message="please, enter your password")])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
