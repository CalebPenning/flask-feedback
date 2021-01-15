from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import email_validator

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)
    
class User(db.Model):
    """Creates user instance for our db/app"""
    __tablename__ = 'users'
    
    username = db.Column(db.Text,
                         primary_key=True,
                         unique=True,
                         nullable=False)
    
    password = db.Column(db.Text,
                         nullable=False)
    
    email = db.Column(db.Text,
                      nullable=False,
                      unique=True)
    
    first_name = db.Column(db.Text,
                           nullable=False,
                           default="")
    
    last_name = db.Column(db.Text,
                           nullable=False,
                           default="")
    
    def __repr__(self):
        u = self
        return f"<User: {u.username}, Email: {u.email}, Name: {u.first_name} {u.last_name}>"
    
    @classmethod
    def register_user(cls, form):
        """Sign up user with hashed password"""
        # Grab all form inputs
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        
        #Hash password into byte string 
        hashed = bcrypt.generate_password_hash(password)
        
        hashed_utf8 = hashed.decode("utf8")
        
        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)
    
    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that the user exists in our database, then compare passwords. 
        If there's a match, return user instance. Otherwise, return False."""
        u = User.query.filter_by(username=username).first()
        
        if u and bcrypt.check_password_hash(u.password, pwd):
            return u
        else:
            return False
        

class Feedback(db.Model):
    __tablename__ = 'feedback'
    
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   unique=True)
    
    title = db.Column(db.Text,
                      nullable=False,
                      unique=False)
    
    content = db.Column(db.Text,
                        nullable=False,
                        unique=False)
    
    username = db.relationship('User', backref='feedback')