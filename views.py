from datetime import datetime
#import uuid

import pytz
import config
import db_config
from flask import Blueprint, flash,request,render_template,redirect, url_for,session

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
            return redirect(url_for('views.common_room'))
    elif not db_config.check_username_exists(username):
        db_config.add_user(username,password,now,crr_ip)
        flash("Login successful")
        return redirect(url_for('views.common_room'))
    elif db_config.check_username_exists(username) and not db_config.password_correct(username,password):
        flash("Wrong pass")
        return redirect(url_for('views.login',wrong_pass=['true']))
    

@views.route('/',methods=['GET','POST'])
def login():
    if session['logged_in']:
        return redirect(url_for('views.common_room'))
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



#/path rest check if guy is in database . if he is give him the username and redirect to common room if not login