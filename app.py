from flask import Flask, flash, request, redirect, render_template, jsonify, session
from models import User, db, bcrypt, connect_db
from forms import AddUserForm
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

@app.route('/')
def index_route():
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = AddUserForm()
    
    if form.validate_on_submit():
        new_user = User.register_user()
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