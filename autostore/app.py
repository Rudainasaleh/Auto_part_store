

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
    database = 'Autostore',
    user = 'postgres',
    password = 'Rudaina998642642',
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

   
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        print(username)
        print(password)
 
        cursor.execute('SELECT * FROM login WHERE username = %s', (username,))
        user_account = cursor.fetchone()

        
        if user_account:
            user_password = user_account['password']
            print(user_password)
            # If account exists in users table in out database
            if ( user_password == password) :
                # Create session data, we can access this data in other routes

                return redirect(url_for('index'))
            else:
                # Account doesnt exist or username/password incorrect
                flash('Incorrect username/password')
        else:
            # Account doesnt exist or username/password incorrect
            flash('Incorrect username/password')
 
    return render_template('login.html')    





    return render_template('login.html')


@app.route('/cart.html', methods=['POST'])
def cart():

    
    quantity = int(request.form['POST'])
    part_quantity = int(request.form['quantity'])
    _code = request.form['code']
    # validate the received values



    return render_template('cart.html')

@app.route('/register.html')
def register():

    
   



    return render_template('register.html')





if __name__ == "__main__":
    app.run(debug = True)
