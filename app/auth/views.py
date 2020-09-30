from flask import render_template,redirect,url_for, flash,request
from . import auth
from ..models import User
from .. import db
from flask_login import login_user,logout_user,login_required
from .forms import LoginForm,RegistrationMerchantForm,RegistrationClerkForm


@auth.route('/login',methods=['GET','POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email = login_form.email.data).first()
        if user is not None and user.verify_password(login_form.password.data):
            login_user(user,login_form.remember.data)
            
            return redirect(request.args.get('next') or url_for('main.index'))

        flash('Invalid username or Password')

    title = "User login"
    return render_template('auth/login.html',login_form = login_form,title=title)


@auth.route('/register/merchant',methods = ["GET","POST"])
def register_merchant():
    form = RegistrationMerchantForm()
    if form.validate_on_submit():
        user = User(email = form.email.data, role = form.role.data,username = form.username.data,password = form.password.data,profile_pic_path= 'photos/unknown.png')
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('auth.login'))
        title = "New Account"
    return render_template('auth/register_merchant.html',registration_form = form)


@auth.route('/register/clerk',methods = ["GET","POST"])
def register_clerk():
    form = RegistrationClerkForm()
    if form.validate_on_submit():
        user = User(email = form.email.data, role = form.role.data,username = form.username.data,password = form.password.data,profile_pic_path= 'photos/unknown.png')
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('auth.login'))
        title = "Register clerk Account"
    return render_template('auth/register_clerk.html',registration_form = form,title=title)         



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))