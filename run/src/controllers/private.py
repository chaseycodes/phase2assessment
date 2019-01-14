#!/usr/bin/env python3


import os

from flask import Blueprint,render_template,request,redirect,url_for,session,flash
from time import gmtime, strftime
#from werkzeug.utils import secure_filename

from ..models.world import User,Posts
# from ..src import ALLOWED_EXTENSIONS, allowed_file 

dratini = Blueprint('private',__name__,url_prefix='/private')

UPLOAD_FOLDER = '/Users/ahn.ch/Desktop/mock_facebook-master/app/run/src/uploads/user'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# @link.before_request
# def before_request():
#     g.username = None
#     if session['username']:
#         g.username = session['username']

@dratini.route('/account',methods=['GET','POST'])
def account():
    un = User(username=session['username'],password=session['password'])
    user_posts  = un.get_posts()
    time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    if request.method == 'GET':
        try:
            return render_template('private/account.html',posts=user_posts)
        except TypeError:
            return render_template('private/account.html')
    elif request.method == 'POST':
        if request.form['posts_button'] == 'Post':
            #FIXME CHECK FOR FILENAME
            content = request.form['post_text']
            filename = str(request.form['img_text'])
            dirlist = os.listdir(UPLOAD_FOLDER)
            if filename in dirlist:
                un.make_post(content,time,filename)
                return redirect('private/account')
            else:
                return render_template('private/account.html',message='You have not uploaded that file yet',posts=user_posts)
        elif request.form['posts_button'] == 'Upload':
            return redirect('/save_file')
        elif request.form['posts_button'] == 'Logout':
            return redirect('private/log-out')
        else:
            list_post_no = request.form['posts_button'].split()
            post_no = list_post_no[1]
            filename = un.get_filename(post_number=post_no)
            return redirect(url_for('display_file', filename=filename))
    else:
        pass

@dratini.route('/log-out')
def logout():
    print(session)
    session.pop('username',None)
    print(session)
    return redirect(url_for('public.index'))

@dratini.route('/dashboard',methods=['GET','POST'])
def dashboard():
    un = User(username=session['username'],password=session['password'])
    if request.method == 'GET':
        try:
            all_posts = un.get_every_post()
            return render_template('private/dashboard.html',posts=all_posts)
        except TypeError:
            return render_template('private/dashboard.html')
    elif request.method == 'POST':
        if request.form['posts_button'] == 'search1':
            try: 
                x = request.form['content']
                posts = un.search_keywords(x)
                return render_template('private/dashboard.html',posts=posts)
            except TypeError:
                return render_template('private/dashboard.html',message='No posts found')
        elif request.form['posts_button'] == 'search2':
            try: 
                user = request.form['user']
                posts = un.get_user_posts(user)
                return render_template('private/dashboard.html',posts=posts)
            except TypeError:
                return render_template('private/dashboard.html',message='No user found or user has not tweeted')
        else:
            list_post_no = request.form['posts_button'].split()
            post_no = list_post_no[1]
            filename = un.get_filename(post_number=post_no)
            un.repost(post_number=post_no,username=session['username'],filename=filename)
            return render_template('private/dashboard.html',message='Reposted to your account')