from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)
    
class User(db.Model):
    """Creates user instance for our db/app"""
    __tablename__ = 'users'
    
    username = db.Column(db.Text(20),
                         primary_key=True,
                         unique=True,
                         nullable=False)
    
    password = db.Column(db.Text,
                         nullable=False)
    
    email = db.Column(db.Text(50),
                      nullable=False,
                      unique=True)
    
    first_name = db.Column(db.Column(30),
                           nullable=False)
    
    last_name = db.Column(db.Column(30),
                           nullable=False)
    
    def __repr__(self):
        u = self
        return f"<User: {u.username}, Email: {u.email}, Name: {u.first_name} {u.last_name}>"
    
    @classmethod
    def register_user(cls):
        """Sign up user with hashed password"""
        # Grab all form inputs
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        
        #Hash password into byte string 
        hashed = bcrypt.generate_password_hash(pwd)
        
        hashed_utf8 = hashed.decode("utf8")
        
        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)