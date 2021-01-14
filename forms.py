from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import InputRequired, Email, email_validator, Length, Optional

class AddUserForm(FlaskForm):
    """Form for creating a new user instance"""
    
    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=20)])
    
    password = PasswordField("Password", validators=[InputRequired(), Length(min=1)])
    
    email = StringField("Email Address", validators=[Email(), Length(min=1, max=50)])
    
    first_name = StringField("First Name", validators=[Optional(), Length(min=0, max=30)])
    
    last_name = StringField("Last Name", validators=[Optional(), Length(min=0, max=30)])

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    
    password = PasswordField("Password", validators=[InputRequired()])

