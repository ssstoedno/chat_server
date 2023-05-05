from datetime import timedelta
from flask import Flask


session_time=timedelta(hours=10)

app=Flask(__name__)
app.config['SECRET_KEY'] = 'verysecretke'
app.permanent_session_lifetime = session_time



