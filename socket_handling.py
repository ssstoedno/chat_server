from datetime import datetime, timedelta
from flask import request, session
import pytz
import config
import db_config
from flask_socketio import SocketIO, send, emit, join_room, leave_room



active_users = []
messages={}
socketio = SocketIO(config.app,async_mode='eventlet')




@socketio.on('join')
def handle_join2(data):
    username=session.get('user_id')
    if username and db_config.is_logged(username):
        emit('timed_out', username)
    else:
        #db_config.update_isactive(username,True)
        now = datetime.utcnow().replace(tzinfo=pytz.UTC)
        session['last_time_access']=now
        if username not in active_users:
            active_users.append(username)
            db_config.update_isactive(username,True)
        join_room(data['room'])
        print(f"{session.get('user_id')} joined {data['room']}")
        emit('user joined', {'username': username}, broadcast=True)
        emit('update active users', {'users': active_users}, broadcast=True) 
    



@socketio.on('leave')
def handle_leave():
    username=session.get('user_id')
    crr_ip=request.remote_addr
    leave_room('common_room')
    if username in active_users:
         if db_config.is_logged(username) and db_config.logged_from_same_ip(username,crr_ip):
            db_config.update_isactive(session['user_id'],False)
            active_users.remove(username)
    emit('timed_out', username)
    emit('update active users', {'users': active_users}, broadcast=True)

@socketio.on('message')
def handle_message(data):
    now:datetime
    expiry:datetime
    username = session.get('user_id')
    now = datetime.utcnow().replace(tzinfo=pytz.UTC) 
    expiry = session['last_time_access'].replace(tzinfo=pytz.UTC) + config.session_time
    if expiry<now:
        emit('timed_out',username)
    else:
        session['last_time_access']=now
        message = data['message']
        emit('message', {'username': username, 'message': message}, room='common_room')
        
