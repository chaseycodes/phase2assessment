#!/usr/bin/env python3

import sqlite3

from flask import session
from random import randint
from time import gmtime, strftime, sleep

from ..mappers.opencursor import OpenCursor


class User:
    def __init__(self, row={}, username='', password=''):
        if username:
            self.check_cred(username,password)
        else:
            self.row_set(row)

    def __enter__(self):
        return self

    def __exit__(self,exception_type,exception_value,exception_traceback):
        sleep(randint(10,10000)/10000)

    def row_set(self,row={}):
        row               = dict(row)
        self.pk           = row.get('pk')
        self.username     = row.get('username')
        self.password     = row.get('password')

    def check_cred(self,username,password):
        with OpenCursor() as cur:
            SQL = """ SELECT * FROM users WHERE
                  username=? and password=?; """
            val = (username,password)
            cur.execute(SQL,val)
            row = cur.fetchone()
        if row:
            self.row_set(row)
        else:
            self.row_set({})

    def check_un(self,username):
        with OpenCursor() as cur:
            SQL = """ SELECT username FROM users WHERE
                  username=?; """
            val = (username,)
            cur.execute(SQL,val)
            row = cur.fetchone()
        if row:
            return True
        else:
            return False

    def login(self,password):
        with OpenCursor() as cur:
            cur.execute('SELECT password FROM users WHERE username=?;',(self.username,))
            if password == cur.fetchone()['password']:
                return True
            else:
                return False
    
    def create_user(self,username,password):
        self.username = username
        self.password = password
        with OpenCursor() as cur:
            SQL = """ INSERT INTO users(
                username,password) VALUES (
                ?,?); """
            val = (self.username,self.password)
            cur.execute(SQL,val)
    
    def make_post(self,text,ts,filename):
        if filename == None:
            self.filename = None
        p          = Posts()
        p.content  = text
        p.time     = ts
        p.username = session['username']
        p.users_pk = self.pk
        p.filename = filename
        p.save()
 
    def get_posts(self):
        try:
            with OpenCursor() as cur:
                SQL = """ SELECT * FROM posts WHERE users_pk=? ORDER BY time DESC limit 10; """
                val = (self.pk,)
                cur.execute(SQL,val)
                data = cur.fetchall()
            if data:
                return [Posts(rows) for rows in data]
        except TypeError:
            return render_template('private/account.html')

    def get_user_posts(self,username):
        with OpenCursor() as cur:
            SQL = """ SELECT * FROM posts WHERE username=? ORDER BY time DESC limit 10; """
            val = (username,)
            cur.execute(SQL,val)
            data = cur.fetchall()
        if data:
            return [Posts(rows) for rows in data]
    
    def search_keywords(self,x):
        with OpenCursor() as cur:
            SQL = """ SELECT * FROM posts WHERE content like '%{}%'; """.format(x)
            cur.execute(SQL,)
            data = cur.fetchall()
        if data:
            return [Posts(rows) for rows in data]
    
    def get_every_post(self):
        with OpenCursor() as cur:
            SQL = """ SELECT * FROM posts ORDER BY time DESC limit 10; """
            cur.execute(SQL,)
            data = cur.fetchall()
        if data:
            return [Posts(rows) for rows in data]
    
    def repost(self, post_number,username,filename):
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        with OpenCursor() as cur:
            SQL = """ SELECT * FROM posts WHERE pk = ?
                    ORDER BY time DESC; """
            cur.execute(SQL, (post_number,))
            row = cur.fetchone()
            post = Posts()
            post.users_pk = self.pk
            post.content = 'Retweeted:'+str(row[1])
            post.username = username
            post.time = time
            post.filename = filename
            post.save()

    def get_filename(self, post_number):
        with OpenCursor() as cur:
            SQL = """ SELECT * FROM posts WHERE pk = ?
                    ORDER BY time DESC; """
            cur.execute(SQL, (post_number,))
            row = cur.fetchone()
            return row[5]

class Posts:

    def __init__(self, row={}):
        # print(row)
        # dict(row)
        if row:
            self.pk       = row[0]
            self.content  = row[1]
            self.time     = row[2]
            self.username = row[3]
            self.users_pk = row[4]
            self.filename = row[5]
        else:
            self.pk = None
            self.content = None
            self.time = None
            self.user_pk = None
            self.username = None
            self.filename = None

    def __bool__(self):
        return bool(self.pk)
    
    #FIXME
    def delete_post(self):
        with OpenCursor() as cur:
            SQL = """ DELETE FROM posts WHERE pk = ?; """
            print(self.pk)
            val = (self.pk,)
            cur.execute(SQL,val)

    
    def save(self):
        with OpenCursor() as cur:
            SQL = """ INSERT INTO posts(
                content,time,username,users_pk,filename
                ) VALUES (?,?,?,?,?); """
            val = (self.content,self.time,self.username,self.users_pk,self.filename)
            cur.execute(SQL,val)

    def __repr__(self):
        output = '{}@{}: {}'
        return output.format(self.username,self.time,self.content)