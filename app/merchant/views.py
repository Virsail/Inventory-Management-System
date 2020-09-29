from . import merchant
from flask import render_template, url_for


@merchant.route('/administrators')
def admin():
  return render_template('merchant/merchant_home.html')


@merchant.route('/administrators/administrator')
def admin_name():
  return render_template('merchant/admin_merchant.html')