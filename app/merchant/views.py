from . import merchant
from flask import render_template, url_for, flash, redirect
from .forms import MerchantRegistrationForm


@merchant.route('/clerks')
def clerks():
  return render_template('merchant/merchant_home.html')


@merchant.route('/administrators/administrator')
def clerk_name():
  return render_template('merchant/admin_merchant.html')


@merchant.route('/stores')
def stores():
  return render_template('merchant/stores.html')


@merchant.route('/register', methods=['GET', 'POST'])
def register():
  form = MerchantRegistrationForm()
  if form.validate_on_submit():
    flash('A registration request has been sent successfully!', 'success')
    return redirect(url_for('merchant.admin'))
  return render_template('merchant/register.html', title='Register Administrator', form=form)

