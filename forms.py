from wtforms import PasswordField, StringField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email

class NewUserForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])

    submit_button = SubmitField("SUBMIT")

class LoginUserForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    
    submit_button = SubmitField("SUBMIT")