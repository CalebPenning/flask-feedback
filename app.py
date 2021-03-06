from flask import Flask, flash, request, redirect, render_template, jsonify, session
from models import User, db, bcrypt, connect_db, Feedback
from forms import AddUserForm, LoginForm, FeedbackForm
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
    
    if 'user_id' in session:
        username = session['user_id']
        flash("You are already registered and signed in.", "warning")
        return redirect(f"/users/{username}")
    
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
        return redirect(f'/users/{new_user.username}')
    
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
            return redirect(f'/users/{user.username}')
        
        else:
            form.username.errors = ['Invalid username or password.']
    
    if 'user_id' in session:
        return redirect(f"/users/{session['user_id']}")
    
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

@app.route('/users/<username>')
def get_user_details(username):
    if 'user_id' in session:
        user = User.query.filter_by(username=username).first()
        feedback = Feedback.query.filter_by(username=username).all()
        return render_template('user_details.html', user=user, feedback=feedback)
    
    else:
        flash("You do not have permission to view that page.", "warning")
        return redirect('/login')
    
@app.route('/users/<username>/delete', methods=['POST'])
def delete_ur_account(username):
    if 'user_id' in session and username == session['user_id']:
        user = User.query.filter_by(username=username).first()
        db.session.delete(user)
        db.session.commit()
        flash("Account deleted. Sorry to see you go.", "primary")
        return redirect('/register')
    
    if 'user_id' in session:
        flash("You don't have permission to do that.", "danger")
        curr_user = session['user_id']
        return redirect(f"/users/{curr_user}")
    
    else:
        flash("Must be logged in to delete account.", "warning")
        return redirect('/login')

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def show_feedback_form(username):
    form = FeedbackForm()
    
    if form.validate_on_submit():
        curr_user = session['user_id']
        Feedback.send_feedback(form, curr_user)
        flash("Feedback sent successfully", "success")
        return redirect(f"/users/{username}")
    
    if 'user_id' in session:
        to_user = User.query.filter_by(username=username).first()
        from_user = User.query.filter_by(username=session['user_id']).first()
        return render_template('feedback_form.html', to_user=to_user, from_user=from_user, form=form)
    
    flash("Please log in to send feedback", "warning")
    return redirect('/login')

@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])
def update_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    form = FeedbackForm(obj=feedback)
    
    if form.validate_on_submit() and session['user_id'] == feedback.username:
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()
        
        flash("Feedback edited successfully.")
        return redirect(f"/users/{feedback.username}")
    
    elif session['user_id'] == feedback.username:
        return render_template('edit_feedback.html', form=form, feedback=feedback)
    
    elif 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect('/login')
    
    else:
        flash("You do not have permission to do anything on our site. Sign up.", "danger")
        return redirect('/register')

