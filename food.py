from flask import Flask,render_template,request, redirect, url_for,session
import sqlite3

app=Flask(__name__)
app.secret_key='123456789'
conn = sqlite3.connect('food.db',check_same_thread=False)
c = conn.cursor()

#Create Database Tables if they do not exist
c.execute('''CREATE TABLE IF NOT EXISTS customers (CustomerId INTEGER PRIMARY KEY AUTOINCREMENT, CustomerName VARCHAR(100),Phone VARCHAR(10),Street VARCHAR(50),City VARHCAR(50),State VARCHAR(50),Pincode INTEGER,Email VARCHAR(50),Password VARCHAR(15))''')
c.execute('''CREATE TABLE IF NOT EXISTS restaurants (RestaurantId INTEGER PRIMARY KEY AUTOINCREMENT, RestaurantName VARCHAR(100),Phone VARCHAR(10),Street VARCHAR(50),City VARHCAR(50),State VARCHAR(50),Pincode INTEGER,Email VARCHAR(50),Password VARCHAR(15),DeliveryFee INTEGER NOT NULL)''')
conn.commit()
c.execute('''CREATE TABLE IF NOT EXISTS items(ItemId INTEGER PRIMARY KEY AUTOINCREMENT,RestaurantId INTEGER,ItemName VARCHAR(100),Price INTEGER,Contents VARCHAR(200),PreparationTime INTEGER,FOREIGN KEY (RestaurantId) REFERENCES restaurants(RestaurantId))''')
conn.commit()
c.execute('''CREATE TABLE IF NOT EXISTS carts (CartId INTEGER PRIMARY KEY AUTOINCREMENT,CustomerId INTEGER,RestaurantId INTEGER,ItemId INTEGER,ItemName VARCHAR(100),Price INTEGER,FOREIGN KEY (CustomerId) REFERENCES customers(CustomerId),FOREIGN KEY (RestaurantId) REFERENCES restaurants(RestaurantId),FOREIGN KEY (ItemId) REFERENCES items(ItemId))''')
conn.commit()

#Login Page
@app.route('/',methods=['POST','GET'])
@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        phone = request.form['username']
        password = request.form['password']
        user_type = request.form['user_type']
        #Get Customer Name if Customer is logging in
        if user_type == 'Customer':
            c.execute("SELECT * FROM customers WHERE phone = ? AND password = ?", (phone, password))
        #Get Restaurant Name if Restaurant is logging in
        else:
            c.execute("SELECT * FROM restaurants WHERE phone = ? AND password = ?", (phone, password))
        account=c.fetchone()
        conn.commit()
        if account:
            session['loggedin'] = True
            session['username'] = account[1]
            #Render user_home.html if user is logging in
            if user_type == 'Customer':
                session['UserId'] = account[0]
                return redirect("user_home")
            #Render restaurant_home.html with restaurant name if restaurant is logging in
            else:
                session['RestId'] = account[0]
                return redirect("/restaurant_home")
        # if no account is found say Incorrect ID / Pass
        else:
            return render_template('login.html',msg= "Incorrect Phone Number/Password")
    return render_template ('login.html')

#Register Page
@app.route('/register',methods=['POST','GET'])
def register():
    if request.method == 'POST':
        user_type=request.form['user_type']
        name = request.form['name']
        phone = request.form['phone']
        street = request.form['street']
        city = request.form['city']
        state = request.form['state']
        pincode = request.form['pincode']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        delivery_fee=request.form['delivery_fee']
        #Insert user only if both passwords match
        if password == confirm_password:
            #If user_type is customer add user info to customers table
            if user_type == 'Customer':
                c.execute("INSERT INTO customers VALUES (NULL,?,?,?,?,?,?,?,?)",(name,phone,street,city,state,pincode,email,password))
            #If user_type is Restaurant add info to restarurants table
            else:
                if delivery_fee:
                    c.execute("INSERT INTO restaurants VALUES (NULL,?,?,?,?,?,?,?,?,?)",(name,phone,street,city,state,pincode,email,password,delivery_fee))
                else:
                    return render_template('register.html',msg="Delivery Fee is required")
        #If passwords do not match
        else:
            return render_template('register.html',msg="Both Passwords do not match")
        conn.commit()
        return render_template ('login.html')
    return render_template ('register.html')

#User Home Page
@app.route('/user_home',methods=['POST','GET'])
def user_home():
    CustId=session['UserId']
    c.execute("SELECT * FROM customers WHERE CustomerId=?",(CustId,))
    conn.commit()
    user=c.fetchone()
    c.execute("SELECT * FROM restaurants")
    conn.commit()
    restaurants=c.fetchall()
    if request.method == 'POST'and request.form['action']=='Order':
        RestId=request.form['RestId'] 
        RestName=request.form['RestName']
        session['RestId']=RestId
        session['RestName']=RestName
        return redirect('/menu')
    elif request.method == 'POST'and request.form['action']=='logout':
        return redirect('/logout')
    return render_template('user_home.html',profile=user[1],restaurants=restaurants)

#Restaurant Home Page
@app.route('/restaurant_home',methods=['POST','GET'])
def restaurant_home():
    RestId=session['RestId']
    c.execute("SELECT * FROM items WHERE RestaurantId=?",(RestId,))
    conn.commit()
    menus=c.fetchall()
    if request.method == 'POST' and request.form['action'] == 'Add':
        ItemName=request.form['name']
        ItemContents=request.form['contents']
        ItemPrice=request.form['price']
        PrepTime=request.form['preparation_time']
        try:
            c.execute("INSERT INTO items VALUES(NULL,?,?,?,?,?)",(RestId,ItemName,ItemPrice,ItemContents,PrepTime))
            conn.commit()
            return redirect('/restaurant_home')
        except: 'There was an issue adding your item'
        return redirect('/restaurant_home')
    elif request.method == 'POST' and request.form['action'] == 'Remove':
        itemId = request.form['MenuId']
        try:
            c.execute('DELETE FROM items where ItemId=?',itemId)
            conn.commit()
            return redirect('/restaurant_home')
        except: 'There was an issue removing your item'
        return redirect('/restaurant_home')
    elif request.method == 'POST'and request.form['action']=='logout':
        return redirect('/logout')
    return render_template('restaurant_home.html',restaurant=session['username'],menus=menus)

@app.route('/menu',methods=['POST','GET'])
def menu():
    RestId=session['RestId']
    RestName=session['RestName']
    UserId=session['UserId']
    c.execute("SELECT * FROM items WHERE RestaurantId=?",(RestId,))
    conn.commit()
    items=c.fetchall()
    if request.method == 'POST' and request.form['action'] == 'Add to Cart':
        ItemId=request.form['ItemId']
        ItemName=request.form['ItemName']
        c.execute("SELECT Price from items where ItemId=?",(ItemId,))
        conn.commit()
        Price=c.fetchone()
        c.execute("INSERT INTO carts VALUES(NULL,?,?,?,?,?)",(UserId,RestId,ItemId,ItemName,Price[0]))
        conn.commit()
        return redirect('/menu')
    if request.method == 'POST' and request.form['action'] == 'Go to Cart':
        return redirect('/cart')
    return render_template('menu.html',restaurant=RestName,items=items)
#cart route
@app.route('/cart',methods=['POST','GET'])
def cart():
    c.execute("SELECT * FROM carts")
    conn.commit()
    cartItems=c.fetchall()
    c.execute("SELECT SUM(Price) FROM carts")
    conn.commit()
    tax=0.05
    total=c.fetchone()
    Ordertotal=total[0]
    tax=round(Ordertotal*0.05,3)
    Ordertotal=Ordertotal+tax
    if request.method == 'POST' and request.form['action']=='logout':
        return redirect('logout')
    elif request.method == 'POST' and request.form['action']=='place Order':
        pass
    return render_template('cart.html',items=cartItems,restaurant=session['RestName'],total=Ordertotal,tax=tax)
#logout route
@app.route('/logout',methods=['POST','GET'])
def logout(): 
    session.pop('logged_in', None)
    return render_template('login.html')

if __name__== '__main__':
    app.run(host='0.0.0.0',debug=True)
