from datetime import timedelta
from flask import Flask
#from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SECRET_KEY'] = 'verysecretkey'
app.permanent_session_lifetime = timedelta(hours=10)


#db:SQLAlchemy()
