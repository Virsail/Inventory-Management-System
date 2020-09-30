from flask import render_template,abort,request,redirect,url_for,flash
from . import clerk
from flask_login import login_required,current_user
from ..models import Product,OrderReceived
from .. import db
# Views
@clerk.route('/',methods= ['GET','POST'])
@login_required
def index():

    '''
    View root page function that returns the clerk index page and its data
    '''
    if request.method=='POST':
        product_name=request.form['product_name']
        product_buying_price=int(request.form['product_buying'])
        product_selling_price=int(request.form['product_selling'])
        order_quantity=int(request.form['order_quantity'])
        order_payment=request.form['order_pay']
       
        order_amount=product_buying_price*order_quantity
        
        new_order=OrderReceived(product_name=product_name,order_quantity=order_quantity,order_payment=order_payment,order_total_amount=order_amount,user=current_user)
        product = Product.query.filter_by(product_name = product_name).first()
        if product is not None:
            product.product_stock = product.product_stock+order_quantity
            product.product_buying_price=product_buying_price
            product.product_selling_price=product_selling_price
            db.session.add(product)
            db.session.commit()
            new_order.save_order()
        else:    
            new_product=Product(product_name=product_name,product_stock=order_quantity,product_buying_price=product_buying_price,product_selling_price=product_selling_price)
            new_product.save_product()
            new_order.save_order()

        flash('Inventory added','success')
        return redirect(url_for('clerk.index'))
    
    return render_template('clerk/index.html')



@clerk.route('/update/sales')
def update_sales():

    '''
    View root page function that returns the clerk update_sales page and its data
    '''
    

    return render_template('clerk/update_sales.html')


@clerk.route('/products')
def products():

    '''
    View root page function that returns the clerk products page and its data
    '''
    
    return render_template('clerk/products.html')



@clerk.route('/update/product')
def update_product():

    '''
    View root page function that returns the clerk update product page and its data
    '''
    
    return render_template('clerk/update_product.html')                   

