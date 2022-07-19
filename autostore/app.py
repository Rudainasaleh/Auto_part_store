

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





@app.route('/register.html', methods=['GET', 'POST'])
def register():

    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
 
    if ( (request.method == 'POST') and ('firstname' in request.form) and ('lastname' in request.form) and ('username' in request.form) and ('password' in request.form) and ('email' in request.form)):
    # Create variables for easy access
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        
    
        cursor.execute('SELECT * FROM userinfo WHERE username = %s', (username,))
        account_username = cursor.fetchone()
        
        
        
        if account_username:
            flash('Account already exists!')
        else:
            cursor.execute("INSERT INTO userinfo (email,username, password, first_name, last_name ) VALUES (%s,%s,%s,%s, %s)", (email, username, password, first_name, last_name))
            conn.commit()
            return redirect(url_for('index'))
    
    
    



    return render_template('register.html')

@app.route("/login.html", methods = ['GET', 'POST'])
def login():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 

   
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        
        
        
 
        cursor.execute('SELECT * FROM login WHERE username = %s', (username,))
        user_account = cursor.fetchone()

        
        if user_account:
            user_password = user_account['password']
            #print(user_password)
            # If account exists in users table in out database
            if ( user_password == password) :
                
                

                return redirect(url_for('index'))
            else:
                # Account doesnt exist or username/password incorrect
                flash('Incorrect username/password')
        else:
            # Account doesnt exist or username/password incorrect
            flash('Incorrect username/password')
  





    return render_template('login.html')




@app.route("/parts.html", methods=['GET', 'POST'])
def part():

    


    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cursor.execute("SELECT * from parts")
    rows = cursor.fetchall()

    
    if request.method == 'POST':
        if request.form['add_to_cart'] == 'Add to cart':
            partid = request.form['partid']
            cursor.execute("SELECT * from parts WHERE partid = %s", (partid))
            
            
            prudoct = cursor.fetchone()
            name = prudoct['name']
            image = prudoct['image']
            price = prudoct['price']
            quantity = request.form['quantity']
            total_price = price 
            
           
        
            
            cursor.execute("INSERT INTO purches (partid, name, image, price, quantity, total_price) VALUES (%s, %s, %s, %s, %s, %s)", (partid, name, image, price, quantity, total_price))
            conn.commit()
            return redirect(url_for('part'))
    
    return render_template('parts.html', part = rows)



@app.route("/cart.html", methods=['GET', 'POST'])
def cart():

    

    
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cursor.execute("SELECT * from purches")
    rows = cursor.fetchall()



    if request.method == 'POST':
        if request.form['remove'] == 'Remove':
            orderid = request.form['orderid']

            cursor.execute("SELECT * from purches WHERE partid = %s", (orderid))
        

            #delete_from_cart(orderid)
            cursor.execute("DELETE FROM purches WHERE orderid = (%s) ", (orderid))
            conn.commit()
            return redirect(url_for('cart'))

    cursor.execute("SELECT * from purches")
    purches = cursor.fetchall()

    cursor.execute("INSERT INTO CART () VALUES ")




    return render_template('cart.html', purches = rows)
    

    


@app.route('/delete_from_cart/id',  methods=['GET', 'POST'])
def delete_from_cart(id):
    orderid = request.form['orderid']
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    
    cursor.execute("DELETE FROM purches WHERE partid = %s", (id))
    conn.commit()

    return redirect(url_for('cart'))


@app.route('/checkout')
def checkout():



    return render_template()



if __name__ == "__main__":
    app.run(debug = True)
