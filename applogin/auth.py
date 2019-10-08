#from applogin import applogin
from flask import Blueprint,render_template,redirect,url_for,request,flash
from flask_login import login_user, logout_user,login_required,current_user
from .forms import LoginForm
from .models import User
from werkzeug.security import generate_password_hash,check_password_hash
import datetime
from . import db, login_manager
from pymongo import MongoClient

auth = Blueprint('auth',__name__)
#@auth.route('/login')
#def login():
#    return render_template('login.html')

@auth.route('/signup')
def signup():
	return render_template('signup.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    #user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database
    user = db.users.find_one({"email":str(email)})
    name_check = db.user.find_one({"name":str(name)})

    if user or name_check: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address or name already exists')
        return redirect(url_for('auth.signup'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_mongo_user={
        "email" : str(email),
        "name"  : str(name),
        "password":str(generate_password_hash(password, method='sha256')),
        "date":datetime.datetime.utcnow()
    }
    #new_user = db.users.(email=email, name=name, password=generate_password_hash(password, method='sha256'))
    new_user_id = db.users.insert_one(new_mongo_user).inserted_id
    # add the new user to the database
    #db.session.add(new_user)
    #db.session.commit()
    return redirect(url_for('auth.login'))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    #request.method == 'POST' and 
    print(current_user.is_authenticated)
    print(form.validate_on_submit())
    #print("estoy")
    if request.method == 'POST':
        print("form validated")
        #print(form)
        #print(form.username.data)
        user = db.users.find_one({"email": str(form.username.data)})
        print(user)
        if user and User.validate_login(user['password'], form.password.data):
            user_obj = User(user['_id'])
            print(user['_id'])
            var_ver=login_user(user_obj,remember=form.remember_me.data)#,remember=form.remember_me.data)
            print(var_ver)
            print(current_user.is_authenticated)
            print("user validated")
            flash("Logged in successfully", category='success')
            #return redirect(request.args.get("next")) or url_for("auth.profile")
            #return redirect(url_for('auth.profile'))
            return redirect(url_for('auth.profile'))
        flash("Wrong username or password", category='error')
    print("not validated")
    return render_template('login.html', title='login', form=form)

@auth.route('/profile')
@login_required
def profile():
    return render_template('profile.html',name=current_user.id)