from datetime import datetime
from flask import session
import pytz
from views import views
import config
import socket_handling

config.app.register_blueprint(views,url_prefix="/")

#before every request
@config.app.before_request
def check_session():
    now = datetime.utcnow().replace(tzinfo=pytz.UTC)
    user_id=session.get('user_id')
    if user_id:
        expiry = session['last_time_access'].replace(tzinfo=pytz.UTC) + config.session_time

        if expiry<now:
            session['user_id']=None#random string
            session['last_time_access']=now
            session['logged_in']=False
        else:
            session['last_time_access']=now
    else:
        session['user_id']=None#random string
        session['last_time_access']=now
        session['logged_in']=False


if __name__=='__main__':
    socket_handling.socketio.run(config.app,debug=True, host='0.0.0.0',port=9000)

    #clear ips in app and server.db

