



import curses

from datetime import date
from tkinter.tix import Form
from traceback import print_exc
from unittest import result
from flask import Flask, flash, redirect, request, url_for, session
from flask import render_template

from flask import session
import os
import psycopg2
import psycopg2.extras
from flask_session import Session





app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


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
            
            session['email'] = email
            session['userid'] = account_username['userid']

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
        
        
        
 
        cursor.execute('SELECT * FROM userinfo WHERE username = %s', (username,))
        user_account = cursor.fetchone()

        
        if user_account:
            user_password = user_account['password']
            #print(user_password)
            # If account exists in users table in out database
            if ( user_password == password) :

                cursor.execute('SELECT * FROM userinfo WHERE username = %s', (username,))
                id = cursor.fetchone()
                session['userid'] = id['userid']
                
                

                


                #cursor.execute('INSERT INTO purchase (userid) VALUES (%s)', (userid,))
                #conn.commit()
                #session['userid'] = userid
           
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

    if 'userid' in session:

    


        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute("SELECT * from parts")
        rows = cursor.fetchall()
    
        if request.method == 'POST':

        #cursor.execute("SELECT * from parts")
        #rows = cursor.fetchall()


        
            if request.form['add_to_cart'] == 'Add to cart':

            


                    partid = request.form['partid']
                    print(partid)
                    cursor.execute("SELECT * from parts WHERE partid = %s", (partid,))
            
            
            
                    prudoct = cursor.fetchone()
                #print(product)
                    name = prudoct['name']
                    image = prudoct['image']
                    price = prudoct['price']
                    quantity = request.form['quantity']
                    print(quantity)
                    total_price = price  * float(quantity)

                    userid = session['userid']
                #id = session['userid']

            

                
            
               
                #cursor.execute("UPDATE purchase SET partid = %s, name=%s, image=%s, price=%s, quantity=%s, total_price=%s WHERE userid =%s", (partid, name, image, price, quantity, total_price, id))
                    cursor.execute("INSERT INTO purchase (partid, name, image, price, quantity, total_price, userid) VALUES (%s, %s, %s, %s, %s, %s, %s)", (partid, name, image, price, quantity, total_price, userid))
                    conn.commit()

                    cursor.execute("SELECT * FROM purchase WHERE partid = (%s) AND userid = (%s) ", (partid, userid))
                    part = cursor.fetchall()
                    orderid = part['orderid']

                    cursor.execute("INSERT INTO parts (orderid) VALUES (%s) WHERE partid = (%s)", (orderid, partid))


                    return redirect(url_for('part'))
    else:
        return redirect(url_for('login'))
            
            
                
    
    return render_template('parts.html', part = rows)



@app.route("/cart.html", methods=['GET', 'POST'])
def cart():

    
    
    if 'userid' in session:
    
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


        userid = session['userid']
        cursor.execute("SELECT * from purchase WHERE userid = %s ", (userid,))
        rows = cursor.fetchall()

        cursor.execute("SELECT SUM(price) AS total from purchase WHERE userid = %s ", (userid,))
            
        total = cursor.fetchone()
        t = total['total']
        print(total)

        tax = (0.6) * (t)
        
        total_price = t + tax

        session['tax'] = tax
        session['total'] = t
        session['final_price'] = total_price




        

        if request.method == 'POST':
            if request.form["remove"] == "Remove":

            

                userid = session['userid']
                print(userid)
                orderid = request.form['orderid']
                cursor.execute("SELECT * from parts WHERE orderid = %s", (orderid,))
                product= cursor.fetchone()

                partid  = product['partid']
                cursor.execute("DELETE FROM purchase WHERE partid = (%s) AND userid = (%s) AND orderid = (%s)", (partid, id, orderid,))
                rows_deleted = cursor.rowcount
                conn.commit()
                return redirect(url_for('cart'))



            #userid = session['userid']
            #cursor.execute("SELECT * from cart WHERE userid = %s ", (userid,))
            #cartinfo = cursor.fetchall()
            
            
            
            #session['total'] = total
            

            #cursor.execute("INSERT INTO cart VALUES (%s) ", (total,))

            
            
            #if request.form['remove_item'] == 'Remove':



                #orderid = request.form['orderid']
            
                #cursor.execute("SELECT * from parts WHERE orderid = %s", (orderid,))
            #order = cursor.fetchone()
            #partid = order['partid']
            #id = session['userid']
            #print(orderid)
            #print(id)
            #print(partid)

            #cursor.execute("DELETE FROM purchase WHERE partid = (%s) AND userid = (%s) AND orderid = (%s)", (partid, id, orderid,))
            #rows_deleted = cursor.rowcount
            #conn.commit()
            #return redirect(url_for('cart'))

    #cursor.execute("SELECT * from purchase")
    #purchase = cursor.fetchall()

    # cursor.execute("INSERT INTO CART () VALUES ")
    else:
        return redirect(url_for('login'))




    return render_template('cart.html', purchase = rows, price=t, tax = tax, total_price=total_price)

        

    

    




@app.route('/checkout.html',  methods=['GET', 'POST'])
def checkout():

    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    userid = session['userid']
    cursor.execute("SELECT * from purchase WHERE userid = %s ", (userid,))
    rows = cursor.fetchall()
 
    

    if ( (request.method == 'POST') and ('name' in request.form) and ('card' in request.form) and ('date' in request.form) and ('cvc' in request.form)):

        
        
            
            userid = session['userid']
            name_on_card = request.form['name']
            card_number = request.form['card']
            date = request.form['date']
            cvc = request .form['cvc']
            #total = session['total']
            cursor.execute("SELECT SUM(price) AS total from purchase WHERE userid = %s ", (userid,))
            
            total = cursor.fetchone()
            #t = total['total']
            t = session['final_price']
            


            cursor.execute("INSERT INTO billing (card_name, card_number, exp_date, cvc, userid, total) VALUES (%s, %s, %s, %s, %s, %s)", (name_on_card, card_number, date, cvc, userid, t))
            conn.commit()

            #cursor.execute("SELECT * FROM billing WHERE userid = (%s) AND card_name = (%s) AND total = (%s)", (userid, name_on_card, t))
            #b = cursor.fetchall()
            #billingid = b['id']

            #session['bid'] = billingid

            session['card_name'] = name_on_card
            return redirect(url_for('delivary'))

            


            #cursor.execute("INSERT INTO billing (card_name, card_number, exp_date, cvc, cartid) VALUES (%s, %s, %s, %s, %s)", (name_on_card, card_number, date, cvc, userid))
            #conn.commit()
    
            



            
    
        


    return render_template('checkout.html')

@app.route('/logout')

def logout():
    session.pop('userid', None)
    flash("You are loged out")
    return redirect(url_for('index'))



@app.route('/delivary.html',  methods=['GET', 'POST'])
def delivary():


    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    userid = session['userid']
    
 
    

    if (request.method == 'POST'):



        t =session['final_price']
        name_on_card = session['card_name']

        


            
    
        address1 = request.form['address1']
        state = request.form['state']
        city = request.form['city']
        zip = request.form['zip']

        date = date.today()
        full_address = address1 + state + city + zip

        billingid = session['bid']

        cursor.execute("SELECT id AS bid from billingid WHERE  userid = (%s) AND card_name = (%s) AND total = (%s)", (userid, name_on_card, t))
            
        total = cursor.fetchone()
        billingid = total['bid']

        
            

            
           

            
        cursor.execute("INSERT INTO cart (userid, order_date,total, billingid, address) VALUES (%s, %s, %S, %s, %s)", (userid, date, t, billingid, full_address))
        conn.commit()


        cursor.execute("DELETE FROM purchase WHERE userid = %s", (userid,))
        rows_deleted = cursor.rowcount
        conn.commit()

        return redirect(url_for('index'))
    
    return render_template('delivary.html')
        




if __name__ == "__main__":
    

    app.run(debug = True)
