
import curses
from distutils.log import error
from tkinter.tix import Form
from flask import Flask, flash, redirect, request, url_for
from flask import render_template
import os
import psycopg2
import psycopg2.extras



app = Flask(__name__)

conn = psycopg2.connect(
    host = 'localhost',
    database = '',
    user = '',
    password = '',
    )

@app.route('/')


def index():
    return render_template('index.html')


@app.route("/parts.html", methods=['GET', 'POST'])
def part():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cursor.execute("SELECT * from parts")
    rows = cursor.fetchall()
    return render_template('parts.html', part = rows)

@app.route("/login.html", methods = ['GET', 'POST'])
def login():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 

    if (request.method == 'POST' and 'username' in request.form and 'password' in request.form) :
        username = request.form['usernam']
        password = request.form['password']
        print(username)
        print(password)

        cursor.execute('SELECT * FROM userInfo WHERE username = %s', (username,))
        user_account = cursor.fetchone()

        if user_account:
            password_rs = user_account['password']
            print(password_rs)
            return redirect(url_for('/index.html'))
        
        else:
            flash('Incorrect username/password')






    return render_template('login.html')





if __name__ == "__main__":
    app.run(debug = True)