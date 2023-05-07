from datetime import datetime
#import uuid

import pytz
import config
import db_config
from flask import Blueprint, flash, jsonify,request,render_template,redirect, url_for,session

views=Blueprint(__name__,'views')



@views.route('/process',methods=['GET','POST'])
def process():
    username=request.form['username']
    password=request.form['password']
    crr_ip=request.remote_addr
    now=datetime.utcnow().replace(tzinfo=pytz.UTC)
    if username=="" or password=="":
        return redirect(url_for('views.login',no_char=['true']))
    elif db_config.check_username_exists(username) and db_config.password_correct(username,password):
        if db_config.is_logged(username):
            return redirect(url_for('views.login',already_logged=['true']))
        else:
            session['user_id']=username
            session['last_time_access']=now
            session['logged_in']=True
            #db_config.update_isactive(username,True)
            db_config.update_ip(username,crr_ip)
            flash("Login successful")
            return redirect(url_for('views.common_room',active=['true']))
    elif not db_config.check_username_exists(username):
        db_config.add_user(username,password,now,crr_ip)
        flash("Login successful")
        return redirect(url_for('views.common_room',active=['true']))
    elif db_config.check_username_exists(username) and not db_config.password_correct(username,password):
        flash("Wrong pass")
        return redirect(url_for('views.login',wrong_pass=['true']))
    
@views.route('/process_change_pass',methods=['GET','POST'])
def process_change_pass():
    new_pass=request.form['password']
    user_id=session['user_id']
    if new_pass=="":
        return redirect(url_for('views.change_pass',active=['true'],no_char=['true']))
    elif db_config.password_correct(user_id,new_pass):
        return redirect(url_for('views.change_pass',active=['true'],same=['true']))
    else:
        db_config.change_pass(user_id, new_pass)
        return redirect(url_for('views.change_pass',active=['true'],success=['true']))



@views.route('/',methods=['GET','POST'])
def login():
    if session['logged_in']:
        return redirect(url_for('views.common_room', active=['true']))
    else:
        return render_template('login.html')

@views.route('/common_room')
def common_room():
    if not session['logged_in']:
         return redirect(url_for('views.login'))
    else:
        return render_template('common_room.html')
    

@views.route('/leave')
def leave():
    #db_config.update_isactive(session['user_id'],False)
    session.clear() 
    log_out = request.args.get('logout')
    return redirect(url_for('views.login',logout=[log_out]))

@views.route('/get_username')
def get_username():
    username=session.get('user_id')
    return jsonify({'username':username})


@views.route('/messages', methods=['GET'])
def get_messages():
    # Get the timestamp or message ID from the last connection
    last_timestamp = request.args.get('since')
    if not last_timestamp:
        last_timestamp = 0
    
    # Query the database for messages since the given timestamp or message ID
    messages = db_config.db.session.query(db_config.Message).filter(db_config.Message.timestamp > last_timestamp).all()

    # Create a list of message strings from the database records
    message_list = [(message.sender,message.message,message.timestamp) for message in messages]
    
    # Return the messages as JSON
    return jsonify({'messages': message_list})
#/path rest check if guy is in database . if he is give him the username and redirect to common room if not login

@views.route('/history')
def history():
    if not session['logged_in']:
         return redirect(url_for('views.login'))
    else:
        return render_template('history.html')
    

@views.route('/change_pass')
def change_pass():
    if not session['logged_in']:
         return redirect(url_for('views.login'))
    else:
        return render_template('change_pass.html')
    