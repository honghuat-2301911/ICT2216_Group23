from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import (
    BooleanField,
    DateTimeLocalField,
    FileField,
    HiddenField,
    IntegerField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    NumberRange,
    Optional,
)


class RegisterForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[DataRequired(message="Name is required"), Length(min=2, max=50)],
    )
    email = StringField(
        "Email Address",
        validators=[
            DataRequired(message="Email is required"),
            Email(message="Enter a valid email"),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message="Password is required"),
            Length(min=8, message="Password must be at least 8 characters long"),
        ],
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(message="Please confirm your password"),
            EqualTo("password", message="Passwords must match"),
        ],
    )
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = StringField(
        "Email Address",
        validators=[
            DataRequired(message="Email is required."),
            Email(message="Please enter a valid email address."),
        ],
    )
    password = PasswordField(
        "Password", validators=[DataRequired(message="Password is required.")]
    )
    submit = SubmitField("Sign In")


class SearchForm(FlaskForm):
    query = StringField("Search activities")
    submit = SubmitField("Search")


class FilterForm(FlaskForm):
    sports_checkbox = BooleanField("Sports")
    non_sports_checkbox = BooleanField("Non Sports")
    submit = SubmitField("Filter")


class HostForm(FlaskForm):
    activity_name = StringField("Activity Name", validators=[DataRequired()])
    activity_type = SelectField(
        "Type",
        choices=[
            ("", "Select Activity Type"),
            ("Sports", "Sports"),
            ("Non Sports", "Non Sports"),
        ],
        validators=[DataRequired()],
    )
    skills_req = StringField("Required Skills", validators=[DataRequired()])
    date = DateTimeLocalField(
        "Date", format="%Y-%m-%dT%H:%M", validators=[DataRequired()]
    )
    location = StringField("Location", validators=[DataRequired()])
    max_pax = IntegerField(
        "Max Participants", validators=[DataRequired(), NumberRange(min=1)]
    )
    submit = SubmitField("Host")


class JoinForm(FlaskForm):
    activity_id = HiddenField(validators=[DataRequired()])
    submit = SubmitField("Join")


class PostForm(FlaskForm):
    content = TextAreaField(
        "Share something with your buddies…", validators=[DataRequired()]
    )
    image = FileField("Image (optional)")
    submit = SubmitField("Post")


class CommentForm(FlaskForm):
    comment = StringField("Write a comment…", validators=[DataRequired()])
    submit = SubmitField("Post")


# forms.py
from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    DateTimeLocalField,
    FileField,
    HiddenField,
    IntegerField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Email, Length, Optional


class ProfileEditForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[Optional(), Length(min=6)])
    profile_picture = FileField("Profile Picture")
    remove_profile_picture = BooleanField("Remove current profile picture")
    submit = SubmitField("Save Changes")


class ActivityEditForm(FlaskForm):
    activity_id = HiddenField()
    activity_name = StringField("Activity Name", validators=[DataRequired()])
    activity_type = SelectField(
        "Type",
        choices=[("Sports", "Sports"), ("Non Sports", "Non Sports")],
        validators=[DataRequired()],
    )
    skills_req = StringField("Skills Required", validators=[DataRequired()])
    date = DateTimeLocalField(
        "Date", validators=[DataRequired()], format="%Y-%m-%dT%H:%M"
    )
    location = StringField("Location", validators=[DataRequired()])
    max_pax = IntegerField("Max Participants", validators=[DataRequired()])
    submit = SubmitField("Save Changes")


class PostEditForm(FlaskForm):
    post_id = HiddenField()
    content = TextAreaField("Content", validators=[DataRequired()])
    remove_image = BooleanField("Remove image from post")
    submit = SubmitField("Save Changes")


class DeleteForm(FlaskForm):
    submit = SubmitField("Delete")


class DeleteActivityForm(FlaskForm):
    activity_id = HiddenField("Activity ID", validators=[DataRequired()])
    submit = SubmitField("Delete Activity")


class DeletePostForm(FlaskForm):
    post_id = HiddenField(validators=[DataRequired()])
    submit = SubmitField("Delete Post")
