from flask import render_template,redirect,url_for
from . import main
from flask_login import login_required,current_user

# Views
@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    if current_user.is_authenticated:
        if current_user.role=='Clerk':
            return redirect(url_for('clerk.index'))
        elif current_user.role=='Merchant':
            return redirect(url_for('merchant.index'))
    return render_template('index.html')


@main.route('/dashboard')
def dashboard():
	return render_template('dashboard.html')




