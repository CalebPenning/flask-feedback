from flask import Flask, flash, request, redirect, render_template, jsonify, session
from models import User, db, bcrypt, connect_db
from forms import AddUserForm, LoginForm
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
import os

"""Set up app configurations, including database uri, secret key for heroku deployment later on"""
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgres:///feedback_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'itsasecret')
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def index_route():
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = AddUserForm()
    
    if form.validate_on_submit():
        new_user = User.register_user(form=form)
        db.session.add(new_user)
        
        try:
            db.session.commit()
            
        except IntegrityError:
            form.username.errors.append('Username already exists. Choose another username.')
            return render_template('register.html')
        
        session['user_id'] = new_user.username
        flash("Account created successfully!", "success")
        return redirect('/secret')
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        user = User.authenticate(username, password)
        
        if user:
            flash(f"Welcome back, {user.username}.", "info")
            session['user_id'] = user.username
            return redirect('/secret')
        
        else:
            form.username.errors = ['Invalid username or password.']
    
    if 'user_id' in session:
        return redirect('/secret')
    
    return render_template('login.html', form=form)

@app.route('/logout')
def logout_user():
    session.pop('user_id')
    flash("Goodbye!", "primary")
    return redirect('/login')

@app.route('/secret')
def show_secret_page():
    if 'user_id' in session:
        username = session['user_id']
        user = User.query.filter_by(username=username).first()
        return render_template('secret.html', user=user)
    
    flash("Please login first", "danger")
    return redirect('/login')