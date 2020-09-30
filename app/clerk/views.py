from flask import render_template
from . import clerk

# Views
@clerk.route('/')
def index():

    '''
    View root page function that returns the clerk index page and its data
    '''
    
    return render_template('clerk/index.html')

