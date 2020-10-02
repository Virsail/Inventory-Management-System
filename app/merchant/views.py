from . import merchant
from flask import render_template, url_for, flash, redirect, jsonify
from flask_login import login_required, current_user
from .forms import MerchantRegistrationForm
from ..models import Product, OrderReceived, Sale, ProductRequest, User
from .. import db
import pandas as pd


@merchant.route('/')
@login_required
def index():
    products = Product.query.all()
    sales = Sale.query.all()
    orders = OrderReceived.query.all()
    prod_requests = ProductRequest.query.all()

    items_sold = 0
    stock = 0
    spoilt = 0
    sales_revenue = 0
    orders_cost = 0
    restock_requests = 0

    stock_list = []
    spoilt_list = []
    sales_list = []
    orders_cost_list = []
    items_sold_list = []
    if products:
        for product in products:
            stock_list.append(product.product_stock)
            spoilt_list.append(product.product_spoilt)
        stock = sum(stock_list)
        spoilt = sum(spoilt_list)
    if sales:
        for sale in sales:
            sales_list.append(sale.sale_amount)
            items_sold_list.append(sale.sale_quantity)
        sales_revenue = sum(sales_list)
        items_sold = sum(items_sold_list)
    if orders:
        for order in orders:
            orders_cost_list.append(order.order_total_amount)
        orders_cost = sum(orders_cost_list)
    if prod_requests:
        restock_requests = len(prod_requests)

    return render_template('merchant/dashboard.html',stats=datasets())


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
    products = Product.query.all()
    sales = Sale.query.all()
    orders = OrderReceived.query.all()
    prod_requests = ProductRequest.query.all()

    items_sold = 0
    stock = 0
    spoilt = 0
    sales_revenue = 0
    orders_cost = 0
    restock_requests = 0

    stock_list = []
    spoilt_list = []
    sales_list = []
    orders_cost_list = []
    items_sold_list = []
    if products:
        for product in products:
            stock_list.append(product.product_stock)
            spoilt_list.append(product.product_spoilt)
        stock = sum(stock_list)
        spoilt = sum(spoilt_list)
    if sales:
        for sale in sales:
            sales_list.append(sale.sale_amount)
            items_sold_list.append(sale.sale_quantity)
        sales_revenue = sum(sales_list)
        items_sold = sum(items_sold_list)
    if orders:
        for order in orders:
            orders_cost_list.append(order.order_total_amount)
        orders_cost = sum(orders_cost_list)
    if prod_requests:
        restock_requests = len(prod_requests)

    reports = {
        "products": products,
        "sales": sales,
        "orders": orders,
        "prod_requests": prod_requests,
        "items_sold": items_sold,
        "stock": stock,
        "spoilt": spoilt,
        "sales_revenue": sales_revenue,
        "orders_cost": orders_cost,
        "restock_requests": restock_requests
    }
    return render_template('merchant/store_reports.html', reports=reports)


@merchant.route('/product_requisition')
@login_required
def product_requisition():
    prod_requests = ProductRequest.query.all()

    return render_template('merchant/product_requisition.html', prod_requests=prod_requests)


@merchant.route('/order_payment_status')
@login_required
def order_payment_status():
    orders = OrderReceived.query.all()
    return render_template('merchant/order_payment_status.html', orders=orders)


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
    order = OrderReceived.query.get(order_id)
    order.order_payment = 'Paid'
    db.session.add(order)
    db.session.commit()

    flash(f'Order for {order.product_name} Paid', 'success')
    return redirect(url_for('merchant.order_payment_status'))


@merchant.route('/approve_request/<action>/<product_name>/<prod_req_id>')
@login_required
def approve_request(action, product_name, prod_req_id):
    prod_req = ProductRequest.query.get(prod_req_id)
    product = Product.query.filter_by(product_name=product_name).first()
    if action == 'Approve':
        prod_req.request_status = 'Approved'
        product.product_stock = product.product_stock + prod_req.request_quantity
        db.session.add(prod_req)
        db.session.add(product)
        db.session.commit()
        flash(f'{product.product_name} order approved', 'success')
    else:
        prod_req.request_status = 'Declined'
        db.session.add(prod_req)
        db.session.commit()
        flash(f'{product.product_name} order declined', 'danger')

    return redirect(url_for('merchant.product_requisition'))


@merchant.route('/register', methods=['GET', 'POST'])
def register():
    form = MerchantRegistrationForm()
    if form.validate_on_submit():
        flash('A clerk email registration request has been sent successfully!', 'success')
        return redirect(url_for('merchant.index'))
    return render_template('merchant/register.html', title='Register Administrator', form=form)


@merchant.route('/data', methods=("GET",))
def datasets():
    print("*" * 50)
    sales_query = pd.read_sql_query("SELECT * FROM sales", con=db.engine)
    revenue = sales_query.groupby([sales_query['sale_time'].dt.date])['sale_amount'].sum()
    revenue = revenue.to_json(orient="split",date_format='iso')
    products_query = pd.read_sql_query("SELECT * FROM products", con=db.engine)._get_numeric_data().drop(columns=['id'])
    total_sales = sales_query['sale_amount'].sum()
    for_total_cost = products_query.drop(columns=['product_selling_price'])
    total_cost = ((for_total_cost['product_spoilt'] + for_total_cost['product_stock']) * for_total_cost[
        'product_buying_price']).sum()
    available_stock = products_query['product_stock'].sum()
    product_units_sold_chart = sales_query.groupby([sales_query['sale_time'].dt.date])['sale_quantity'].sum().to_json(orient="split",date_format='iso')
    product_units_sold = sales_query['sale_quantity'].sum()
    data = dict(
        total_cost=int(total_cost),
        available_stock=int(available_stock),
        product_units_sold=int(product_units_sold),
        total_sales=int(total_sales),
        revenue=revenue,
        product_units_sold_chart=product_units_sold_chart,

    )

    # import pdb;
    # pdb.set_trace()
    # return response
    return data

    print(revenue)
    print("*" * 50)
