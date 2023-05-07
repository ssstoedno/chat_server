from datetime import timedelta
from flask import Flask

#create
app=Flask(__name__,template_folder='app/templates', static_folder='app/static')
#session secret key
app.config['SECRET_KEY'] = 'verysecretee'
#set session time
session_time=timedelta(hours=10)
app.permanent_session_lifetime = session_time



