from . import merchant
from flask import render_template, url_for, flash, redirect
from .forms import ClerkRegistrationForm, RegistrationClerkForm
from app import mail
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from flask import current_app
from ..models import User


# s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

@merchant.route('/')
def index():
  return render_template('merchant/dashboard.html')

@merchant.route('/clerks')
def clerks():
  return render_template('merchant/merchant_home.html')



@merchant.route('/administrators/administrator')
def clerk_name():
  return render_template('merchant/admin_merchant.html')


@merchant.route('/stores')
def stores():
  return render_template('merchant/stores.html')

@merchant.route('/stores/westgate')
def westgate_shop():
  return render_template('merchant/stores/westgate.html')

@merchant.route('/store/reports/<store_name>')
def store_reports(store_name):
  return render_template('merchant/store_reports.html')

# def send_registration_email(user):
#   token = user.get_register_token()
#   msg = Message('Registration Form', sender='noreply@demo.com', recipients=[user.email])
#   msg.body = f'''To Register, follow this link
# {url_for('register_token', token=token,_external=True)}'''
#   mail.send(msg)

@merchant.route('/register', methods=['GET', 'POST'])
def register_request():
  s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
  form = ClerkRegistrationForm()
  email = form.email.data
  print(email)
  token = s.dumps(email, salt='email_confirm')
  msg = Message('Register', sender='odhiamboderrick56@gmail.com', recipients=[email])
  link = url_for('merchant.register_clerk', token=token, _external=True)

  msg.body = f"<p>Invitation to register as clerk : <a href='{link}'>{link}</a> </p>"

  mail.send(msg)

  return render_template('merchant/register.html', form=form)

@merchant.route('/register/<token>', methods=['GET', 'POST'])
def register_clerk(token):
  s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
  try:
    email = s.loads(token, salt='email_confirm', max_age=2000)
  except SignatureExpired:
    flash('The token has expired. Contact your employer','danger')
  form = RegistrationClerkForm()
  if form.validate_on_submit():
    user = User(email = form.email.data, role = form.role.data,username = form.full_name.data,password = form.password.data,profile_pic_path= 'photos/unknown.png')
    db.session.add(user)
    db.session.commit()

    return redirect(url_for('auth.login'))
    
  return render_template('auth/register_clerk.html',registration_form = form) 
