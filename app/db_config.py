import config
import os

from flask import session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


# connect to the database
config.app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'server.db')
db = SQLAlchemy(config.app)


class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username=db.Column(db.String(50), unique=True)
        password=db.Column(db.String(50))
        ip=db.Column(db.String(50))
        is_active=db.Column(db.Boolean,default=False, nullable=False)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    sender = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    message = db.Column(db.Text, nullable=False)


with config.app.app_context():
    db.create_all()
    deactivate_users=db.session.query(User).filter_by(is_active=True).all()
    all_messages=db.session.query(Message).all()
    for message in all_messages:
         db.session.delete(message)
         db.session.commit()
    for user in deactivate_users:
        user.is_active=False
        db.session.commit()
    
         
     


def add_user(username,password,last_access,ip):
    session['user_id'] = username
    session['last_time_access'] = last_access # add this line to set the session time
    session['logged_in']=True
    entry=User(username=username,password=password,ip=ip,is_active=False)#last_access_time=last_access)
    db.session.add(entry)
    db.session.commit()



def check_username_exists(username):
    user = db.session.query(User).filter_by(username=username).first()
    if user:
        return True
    else:
         return False


def password_correct(username,password):
     user = db.session.query(User).filter_by(username=username).first()
     if user.password==password:
          return True
     else:
          return False

def update_isactive(username,activity):
     user = db.session.query(User).filter_by(username=username).first()
     user.is_active=activity
     db.session.commit()

def is_logged(username):
     user = db.session.query(User).filter_by(username=username).first()
     if user.is_active:
          return True
     else:
          return False
     
def logged_from_same_ip(username,crr_ip):
     user = db.session.query(User).filter_by(username=username).first()
     if user.ip==crr_ip:
          return True
     else:
          return False

def update_ip(username,crr_ip):
     user = db.session.query(User).filter_by(username=username).first()
     user.ip=crr_ip
     db.session.commit()

def add_message(username,message):
     new_message = Message(sender=username,message=message)
     db.session.add(new_message)
     db.session.commit()

def change_pass(username,new_pass):
     user=db.session.query(User).filter_by(username=username).first()
     user.password=new_pass
     db.session.commit()

def change_user(username,new_user):
     user=db.session.query(User).filter_by(username=username).first()
     user.username=new_user
     db.session.commit()

