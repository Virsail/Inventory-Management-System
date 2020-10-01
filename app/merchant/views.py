from . import merchant
from flask import render_template, url_for, flash, redirect
from flask_login import login_required, current_user
from .forms import MerchantRegistrationForm
from ..models import Product, OrderReceived, Sale, ProductRequest, User
from .. import db


@merchant.route('/')
@login_required
def index():
    print(current_user)
    return render_template('merchant/dashboard.html')


@merchant.route('/clerks')
@login_required
def clerks():

    clerks = User.query.filter_by(role='Clerk').all()

    return render_template('merchant/merchant_home.html', clerks=clerks)


@merchant.route('/clerk/<clerk_name>')
@login_required
def clerk_details(clerk_name):

    clerk = User.query.filter_by(role='Clerk', username=clerk_name).first()

    return render_template('merchant/clerk_details.html', clerk=clerk)


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

    prod_requests=ProductRequest.query.all()

    return render_template('merchant/product_requisition.html',prod_requests=prod_requests)


@merchant.route('/order_payment_status')
@login_required
def order_payment_status():

    orders=OrderReceived.query.all()
    return render_template('merchant/order_payment_status.html',orders=orders)


@merchant.route('/update_status/<clerk_name>')
@login_required
def update_status(clerk_name):
    clerk = User.query.filter_by(role='Clerk', username=clerk_name).first()
    if clerk.status == 'Active':
        clerk.status = 'Inactive'
    else:
        clerk.status = 'Active'
    db.session.add(clerk)
    db.session.commit()
    flash(f'Account Status for {clerk_name} Updated', 'success')
    return redirect(url_for('merchant.clerk_details', clerk_name=clerk_name))




@merchant.route('/delete_clerk/<clerk_name>')
@login_required
def delete_clerk(clerk_name):
    clerk = User.query.filter_by(role='Clerk', username=clerk_name).first()
    db.session.delete(clerk)
    db.session.commit()
   
    flash(f'Account for {clerk_name} Deleted', 'danger')
    return redirect(url_for('merchant.clerks'))   


@merchant.route('/pay_order/<order_id>')
@login_required
def pay_order(order_id):
    order=OrderReceived.query.get(order_id)
    order.order_payment='Paid'
    db.session.add(order)
    db.session.commit()
   
    flash(f'Order for {order.product_name} Paid', 'success')
    return redirect(url_for('merchant.order_payment_status'))       



@merchant.route('/approve_request/<action>/<product_name>/<prod_req_id>')
@login_required
def approve_request(action,product_name,prod_req_id):
    
    prod_req=ProductRequest.query.get(prod_req_id)
    product = Product.query.filter_by(product_name = product_name).first()
    if action=='Approve':
      prod_req.request_status='Approved'
      product.product_stock=product.product_stock+prod_req.request_quantity
      db.session.add(prod_req)
      db.session.add(product)
      db.session.commit()
      flash(f'{product.product_name} order approved','success')
    else:
      prod_req.request_status='Declined'
      db.session.add(prod_req)  
      db.session.commit()
      flash(f'{product.product_name} order declined','danger')

    return redirect(url_for('merchant.product_requisition'))  

@merchant.route('/register', methods=['GET', 'POST'])
def register():
    form = MerchantRegistrationForm()
    if form.validate_on_submit():
        flash('A clerk email registration request has been sent successfully!', 'success')
        return redirect(url_for('merchant.index'))
    return render_template('merchant/register.html', title='Register Administrator', form=form)
