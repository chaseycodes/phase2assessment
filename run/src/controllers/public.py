#!/usr/bin/env python3


import os

from flask import Blueprint,render_template,request,session,redirect,url_for

from ..models.world import User
from ..mappers.opencursor import OpenCursor

dratini = Blueprint('public',__name__,url_prefix='/public')

UPLOAD_FOLDER = '/Users/ahn.ch/Desktop/facebook_mock/app/run/src/uploads'

@dratini.route('/',methods=['GET','POST'])
def index():
    if request.method == 'GET':
        with User() as un:
            all_posts = un.get_every_post()
            return render_template('public/index.html',posts=all_posts)
    elif request.method == 'POST':
        if request.form['posts_button'] == 'Login':
            with User(username=request.form['username'],password=request.form['password']) as un:
                try:
                    if un.login(request.form['password']):
                        session['username'] = un.username
                        session['password'] = un.password
                        session['pk']       = un.pk
                        all_posts = un.get_every_post()
                        return redirect('private/account')
                    else:
                        return render_template('public/index.html',message='Bad Credentials')
                except TypeError:
                    return render_template('public/index.html')
        elif request.form['posts_button'] == 'Register':
            return render_template('public/register.html')
        else:
            pass
    else:
        pass

@dratini.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('public/register.html')
    elif request.method == 'POST':
        with User(username=request.form['username'],password=request.form['password']) as un:
            if un.check_un(request.form['username']):
                return render_template('public/register.html', message='Username Exists')  
            else:
                un.create_user(request.form['username'],request.form['password'])
                user_upload_folder = UPLOAD_FOLDER + '/' + str(request.form['username'])
                os.system('mkdir {}'.format(user_upload_folder))
                return render_template('public/register.html',message='Created Account')
    else:
        return render_template('public/login.html', message='Bad Credentials')  
