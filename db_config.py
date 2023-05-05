import config
import os
import sqlite3

from flask import session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


#if os.path.exists('server.db'):
    #delete the file if it exists
    #os.remove('server.db')


# connect to the database
conn = sqlite3.connect('server.db')
conn.close()
config.app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'server.db')
db = SQLAlchemy(config.app)


class Users(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username=db.Column(db.String(50), unique=True)
        password=db.Column(db.String(50))
        ip=db.Column(db.String(50))
        is_active=db.Column(db.Boolean,default=False, nullable=False)

class Messages(db.Model):
    sender = db.Column(db.String(50), nullable=False)
    recipient = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    message = db.Column(db.Text, nullable=False)
    __table_args__ = (
        db.PrimaryKeyConstraint('sender', 'recipient', 'timestamp'),
    )


with config.app.app_context():
    db.create_all()
    deactivate_users=db.session.query(Users).filter_by(is_active=True).all()
    for user in deactivate_users:
        user.is_active=False
        db.session.commit()
     


def add_user(username,password,last_access,ip):
    session['user_id'] = username
    session['last_time_access'] = last_access # add this line to set the session time
    session['logged_in']=True
    entry=Users(username=username,password=password,ip=ip,is_active=False)#last_access_time=last_access)
    db.session.add(entry)
    db.session.commit()



def check_username_exists(username):
    user = db.session.query(Users).filter_by(username=username).first()
    if user:
        return True
    else:
         return False


def password_correct(username,password):
     user = db.session.query(Users).filter_by(username=username).first()
     if user.password==password:
          return True
     else:
          return False

def update_isactive(username,activity):
     user = db.session.query(Users).filter_by(username=username).first()
     user.is_active=activity
     db.session.commit()

def is_logged(username):
     user = db.session.query(Users).filter_by(username=username).first()
     if user.is_active:
          return True
     else:
          return False
     
def logged_from_same_ip(username,crr_ip):
     user = db.session.query(Users).filter_by(username=username).first()
     if user.ip==crr_ip:
          return True
     else:
          return False

def update_ip(username,crr_ip):
     user = db.session.query(Users).filter_by(username=username).first()
     user.ip=crr_ip
     db.session.commit()
#def update_time(username,now):
    #session['last_time_access']=now
    #user = db.session.query(Users).filter_by(username=username).first()
    #user.last_access_time=now
    #db.session.commit()

#def delete_user(username):
    #user = db.session.query(Users).filter_by(username=username).first()
    #db.session.delete(user)
    #db.session.commit()


