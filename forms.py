from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange


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
    submit = SubmitField('Login')


class ReviewForm(FlaskForm):
    rating = IntegerField('Rating',
                          validators=[DataRequired(message="please, enter your rating"),
                                      NumberRange(min=0, max=5, message="rating limits are 0 and 5")])
    review = StringField('Review', validators=[Length(min=6, max=5000, message="review should be at least 6 charachters and max as 5000")])
    book_id = IntegerField('book_id', validators=[DataRequired()])
    submit = SubmitField('Add review')
