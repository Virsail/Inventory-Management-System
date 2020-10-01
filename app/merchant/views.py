from . import merchant
from flask import render_template, url_for, flash, redirect
from .forms import ClerkRegistrationForm
from ..auth.forms import RegistrationClerkForm
from app import mail
from flask_mail import Message
from ..models import CLerkRegister 

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

def send_registration_email(user):
  token = user.get_register_token()
  msg = Message('Registration Form', sender='noreply@demo.com', recipients=[user.email])
  msg.body = f'''To Register, follow this link
{url_for('register_token', token=token,_external=True)}'''
  mail.send(msg)

@merchant.route('/register', methods=['GET', 'POST'])
def register_request():
  form = ClerkRegistrationForm()
  if form.validate_on_submit():
    user = CLerkRegister.query.filter_by(email=form.email.data).first()
    send_registration_email(user)
    flash('A clerk email registration request has been sent successfully!', 'info')
    return redirect(url_for('merchant.index'))
  return render_template('merchant/register.html', title='Register Administrator', form=form)


@merchant.route('/register/<token>', methods=['GET', 'POST'])
def register_token(token): 
  user = CLerkRegister.verify_register_token(token)
  if user is None:
    flash('That is an invalid token,contact your employer', 'warning')
    return redirect(url_for('main.dashboard'))
  form = RegistrationClerkForm()
  return render_template('auth/register_clerk.html', title='Registration', form = form)