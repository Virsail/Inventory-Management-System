from . import merchant
from flask import render_template, url_for, flash, redirect
from flask_login import login_required,current_user
from .forms import MerchantRegistrationForm

@merchant.route('/')
@login_required
def index():
  print(current_user)
  return render_template('merchant/dashboard.html')

@merchant.route('/clerks')
@login_required
def clerks():
  return render_template('merchant/merchant_home.html')



@merchant.route('/administrators/administrator')
@login_required
def clerk_name():
  return render_template('merchant/admin_merchant.html')


@merchant.route('/stores')
@login_required
def stores():
  return render_template('merchant/stores.html')


@merchant.route('/store/reports/<store_name>')
@login_required
def store_reports(store_name):
  return render_template('merchant/store_reports.html')

@merchant.route('/product_requisition')
@login_required
def product_requisition():
	return render_template('merchant/product_requisition.html')	


@merchant.route('/order_payment_status')
@login_required
def order_payment_status():
	return render_template('merchant/order_payment_status.html')	







@merchant.route('/register', methods=['GET', 'POST'])
def register():
  form = MerchantRegistrationForm()
  if form.validate_on_submit():
    flash('A clerk email registration request has been sent successfully!', 'success')
    return redirect(url_for('merchant.index'))
  return render_template('merchant/register.html', title='Register Administrator', form=form)

