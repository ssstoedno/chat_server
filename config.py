from datetime import timedelta
from flask import Flask

#create
app=Flask(__name__)
#session secret key
app.config['SECRET_KEY'] = 'verysecreteeee'
#set session time
session_time=timedelta(hours=10)
app.permanent_session_lifetime = session_time



