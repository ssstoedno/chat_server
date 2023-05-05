from datetime import datetime, timedelta
from flask import session
import pytz
import config
from flask_socketio import SocketIO, send, emit, join_room, leave_room



active_users = []
messages={}
socketio = SocketIO(config.app,async_mode='eventlet')




@socketio.on('join')
def handle_join2(data):
    now = datetime.utcnow().replace(tzinfo=pytz.UTC)
    username=session.get('user_id')
    session['last_time_access']=now
    if username not in active_users:
        active_users.append(username)
    join_room(data['room'])
    print(f"{session.get('user_id')} joined {data['room']}")
    emit('user joined', {'username': username}, broadcast=True)
    emit('update active users', {'users': active_users}, broadcast=True) 
    



@socketio.on('leave')
def handle_leave():
    username=session.get('user_id')
    leave_room('common_room')
    if username in active_users:
        active_users.remove(username)
    emit('timed_out', username)
    emit('update active users', {'users': active_users}, broadcast=True)

@socketio.on('message')
def handle_message(data):
    now:datetime
    expiry:datetime
    username = session.get('user_id')
    now = datetime.utcnow().replace(tzinfo=pytz.UTC) 
    expiry = session['last_time_access'].replace(tzinfo=pytz.UTC) + timedelta(hours=10)
    
    session['last_time_access']=now
    message = data['message']
    emit('message', {'username': username, 'message': message}, room='common_room')
        
