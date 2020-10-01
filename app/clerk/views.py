from flask import render_template,abort,request,redirect,url_for,flash
from . import clerk
from flask_login import login_required,current_user
from ..models import Product,OrderReceived,Sale,ProductRequest
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



@clerk.route('/update/sales',methods= ['GET','POST'])
@login_required
def update_sales():

    '''
    View update sales page function that returns the clerk update_sales page and its data
    '''
    products=Product.query.all()
    if request.method=='POST':
        product_name=request.form['item_sold']
        quantity_sold=int(request.form['quantity_sold'])
        
        product = Product.query.filter_by(product_name = product_name).first()
        if (product.product_stock-product.product_spoilt)<quantity_sold:
            flash(f'Sorry could not add sale.Stock is {product.product_stock-product.product_spoilt}','danger')
            return redirect(url_for('clerk.update_sales'))
        else:
            total_sale=product.product_selling_price*quantity_sold
            new_sale=Sale(product_name=product_name,sale_quantity=quantity_sold,sale_amount=total_sale,user=current_user)
            new_sale.save_sale()
            product.product_stock= product.product_stock-quantity_sold
            db.session.add(product)
            db.session.commit()
            flash(f'{product_name} sale updated','success')
            return redirect(url_for('clerk.my_sales'))   

    return render_template('clerk/update_sales.html',products=products)


@clerk.route('/products')
@login_required
def products():

    '''
    View product page function that returns the clerk products page and its data
    '''

    products=Product.query.all()
    
    return render_template('clerk/products.html',products=products)



@clerk.route('/update/product/<product_name>',methods= ['GET','POST'])
@login_required
def update_product(product_name):

    '''
    View update product page function that returns the clerk update product page and its data
    '''
    product=Product.query.filter_by(product_name = product_name).first()
    if request.method=='POST':
        product_buying=request.form['product_buying']
        product_selling=request.form['product_selling']
        product_stock=request.form['product_stock']
        product_spoilt=request.form['items_spoilt']

        product.product_buying_price=product_buying
        product.product_selling_price=product_selling
        product.product_stock=product_stock
        product.product_spoilt=product_spoilt

        db.session.add(product)
        db.session.commit()
        flash(f'{product_name} details updated','success')
        return redirect(url_for('clerk.products'))   
    return render_template('clerk/update_product.html',product=product)


@clerk.route('/mysales')
@login_required         
def my_sales():
    '''
    View my sales page function that returns the clerk sales page and its data
    '''
    sales=Sale.query.filter_by(user_id=current_user.id).order_by(Sale.sale_time.desc()).all()      
    return render_template('clerk/sales.html',sales=sales)


@clerk.route('/request/product/<product_name>',methods= ['GET','POST'])
@login_required
def request_product(product_name):

    '''
    View request product page function that returns the form to make a product request
    '''
    product=Product.query.filter_by(product_name = product_name).first()
    if request.method=='POST':
       req_quantity=request.form['request_quantity'] 
       new_request=ProductRequest(product_id=product.id,user_id=current_user.id,request_quantity=req_quantity)
       new_request.save_request()
       flash(f'Request for {req_quantity} {product_name}  has been made','success')
       return redirect(url_for('clerk.my_requests'))   
    return render_template('clerk/request_product.html',product=product)


@clerk.route('/myrequests')
@login_required         
def my_requests():
    '''
    View my request page function that returns the requests page and its data
    '''
    requests=ProductRequest.query.filter_by(user_id=current_user.id).order_by(ProductRequest.request_time.desc()).all()      
    return render_template('clerk/requests.html',requests=requests)    



