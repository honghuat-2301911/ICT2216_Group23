from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class RegisterForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[DataRequired(message="Name is required"), Length(min=2, max=50)]
    )
    email = StringField(
        'Email Address',
        validators=[DataRequired(message="Email is required"), Email(message="Enter a valid email")]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(message="Password is required"), Length(min=8, message="Password must be at least 8 characters long")],
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(message="Please confirm your password"),
            EqualTo('password', message="Passwords must match")
        ]
    )
    skill_lvl = StringField(
        'Skill Level',
        validators=[DataRequired(message="Skill level is required")]
    )
    sports_exp = StringField(
        'Sports Experience',
        validators=[DataRequired(message="Please share your sports experience")]
    )
    submit = SubmitField('Register')
