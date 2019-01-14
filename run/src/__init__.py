#!/usr/bin/env python3

import os
import csv

from flask import Flask,render_template,request,session,redirect,send_from_directory,url_for

from .controllers.private import dratini as private_dragon
from .controllers.public  import dratini as public_dragon

UPLOAD_FOLDER = '/Users/ahn.ch/Desktop/facebook_mock/app/run/src/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
IPFS_HASH='QmW2WQi7j6c7UgJTarActp7tDNikE4B2qXtFCfLPdsgaTQ'
human_readable_address = 'cat.jpg'

dragonite = Flask(__name__)
dragonite.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 

dragonite.register_blueprint(private_dragon)
dragonite.register_blueprint(public_dragon)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

        
def ipfs_request(IPFS_HASH,human_readable_address):
	try:
		with open(human_readable_address, 'r') as file:
			print("Ok")
	except IOError:
		os.system(f'wget --user-agent="Mozilla/5.0" "https://ipfs.io/ipfs/{human_readable_address}/cat.jpg" -O /Users/ahn/Desktop/facebook_mock/run/src/uploads')

# https://ipfs.io/ipfs/<ipfs hash> is the document root	

@dragonite.route('/save_file',methods=['GET','POST'])
def save_file():
    if request.method == 'GET':
        return render_template('private/save_file.html')
    elif request.method == 'POST':
        if request.form['posts_button'] == 'Upload':
            file = request.files['filename']
            filename = str(file.filename)
            if allowed_file(filename):
                file.save(os.path.join(dragonite.config['UPLOAD_FOLDER'], filename))
                #move file to user upload folder
                return render_template('private/save_file.html',message='File Saved')
            else:
                return render_template('private/save_file.html', message='Filetype Not Supported')
        elif request.form['posts_button'] == 'Search':
            pass
        elif request.form['posts_button'] == 'View File':
            filename = request.form['view_filename']
            return redirect(url_for('display_file', filename=filename))
        else:
            pass
    else:
        pass

@dragonite.route('/uploads/<filename>',methods=['GET','POST'])
def display_file(filename):
    return send_from_directory(dragonite.config['UPLOAD_FOLDER'], filename)

@dragonite.errorhandler(404)
def not_found(error):
    return render_template('public/404.html')

def keymaker(registry,filename='secret_key'):
    """registry is an arguement that should 
    be replaced with the Main Flask Mod"""
    pathname = os.path.join(registry.instance_path,filename) #<--THE PATH TO THE SECRET KEY
    try:
        """CHECK FOR THE KEY"""
        registry.config['SECRET_KEY'] = open(pathname,'rb').read() 
        
    except IOError: #inputoutput err
        if not os.path.isdir(os.path.dirname(pathname)):
            os.system('mkdir -p {}'.format(os.path.dirname(pathname)))
        """GENERATE SECRET KEY"""
        os.system(f'head -c 256 /dev/urandom > {pathname}') 
        keymaker(registry) #GENERATE FILE AND TRY AGAIN

keymaker(dragonite)