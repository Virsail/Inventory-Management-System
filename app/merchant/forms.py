from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from ..models import User


class ClerkRegistrationForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired(), Email()])
  submit = SubmitField('Send Request')   


class RegistrationClerkForm(FlaskForm):
    email = StringField('Your Email Address',validators=[DataRequired(),Email()])
    full_name = StringField('Enter your fullname',validators = [DataRequired()])
    role = SelectField(u'Role', choices=[('Clerk', 'Clerk')],validators = [DataRequired()])
    password = PasswordField('Password',validators = [DataRequired(), EqualTo('password_confirm',message = 'Passwords must match')])
    password_confirm = PasswordField('Confirm Passwords',validators = [DataRequired()])
    submit = SubmitField('Sign Up')



    def validate_email(self,data_field):
              '''
              takes in the data field and checks our database to confirm there is no user registered with that email address
              '''
              if User.query.filter_by(email =data_field.data).first():
                  raise ValidationError('There is an account with that email')

    def validate_username(self,data_field):
        '''
        checks to see if the username is unique and raises a ValidationError if another user with a similar username is found.
        '''
        if User.query.filter_by(username = data_field.data).first():
            raise ValidationError('That username is taken')  