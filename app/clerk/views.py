from flask import render_template
from . import clerk

# Views
@clerk.route('/')
def index():

    '''
    View root page function that returns the clerk index page and its data
    '''
    
    return render_template('clerk/index.html')



@clerk.route('/')
def update_sales():

    '''
    View root page function that returns the clerk update_sales page and its data
    '''
    
    return render_template('clerk/update_sales.html')    

