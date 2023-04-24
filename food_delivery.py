import uuid
from flask import Flask,render_template,request, redirect, url_for,session
import sqlite3
from datetime import datetime

app=Flask(__name__)

app.secret_key='123456789'
conn = sqlite3.connect('food_delivery.db',check_same_thread=False)
c = conn.cursor()

RESTAURANT=[{"RestaurantID":1,"Name":"Biryani House","DeliveryFee":5,"City":"Wichita","State":"Ks","PinCode":123455},{"RestaurantID":2,"Name":"Dosa Palace","DeliveryFee":3,"City":"Wichita","State":"Ks","PinCode":123455},{"RestaurantID":3,"Name":"Paradise","DeliveryFee":6,"City":"Wichita","State":"Ks","PinCode":123455},{"RestaurantID":4,"Name":"Bawarchi","DeliveryFee":3,"City":"Wichita","State":"Ks","PinCode":123457}]
MENU=[{"ItemID":1,"Name":"Biryani","Price":15,"Preparation_Time":20,"Description":"Rice Flavoured with Indian Spices"},{"ItemID":2,"Name":"Idli","Price":10,"Preparation_Time":10,"Description":"Steam cooked pan cake batter with dip of tomato chutney"},{"ItemID":3,"Name":"Dosa","Price":5,"Preparation_Time":7,"Description":"pan cake batter with dip of coconut chutney"},{"ItemID":4,"Name":"Tandoori Chicken","Price":15,"Preparation_Time":20,"Description":"Chicken roasted in Tandoor"},{"ItemID":5,"Name":"Grill Chicken","Price":15,"Preparation_Time":20,"Description":"Chicken Grilled on Charcoal"}]

c.execute('''CREATE TABLE IF NOT EXISTS customers (CustomerId INTEGER PRIMARY KEY AUTOINCREMENT, CustomerName VARCHAR(100),Phone VARCHAR(10),Street VARCHAR(50),City VARHCAR(50),State VARCHAR(50),Pincode INTEGER,Email VARCHAR(50),Password VARCHAR(15))''')
c.execute('''CREATE TABLE IF NOT EXISTS restaurants (RestaurantId INTEGER PRIMARY KEY AUTOINCREMENT, RestaurantName VARCHAR(100),Phone VARCHAR(10),Street VARCHAR(50),City VARHCAR(50),State VARCHAR(50),Pincode INTEGER,Email VARCHAR(50),Password VARCHAR(15))''')
conn.commit()
c.execute('''CREATE TABLE IF NOT EXISTS menu(ItemId INTEGER PRIMARY KEY AUTOINCREMENT,RestaurantId INTEGER,Price INTEGER,PreparationTime INTEGER,FOREIGN KEY (RestaurantId) REFERENCES restaurants(RestaurantId))''')
conn.commit()
#Login Page
@app.route("/")
@app.route("/login",methods=['POST','GET'])
def login():
    if request.method=='POST' and 'username' in request.form and 'password' in request.form:
        user_type = request.form['user_type']
        print(user_type)
        phone = request.form['username']
        password = request.form['password']
        #Connect database to check for user
        if user_type == 'Customer':
            username=c.execute("SELECT * FROM customers WHERE phone = ? AND password = ?", (phone, password))
            return render_template('user_home.html')
        elif user_type == 'Restaurant':            
            c.execute("SELECT RestaurantName FROM restaurants WHERE phone = ? AND password = ?", (phone, password))
            username=c.fetchone()
            return render_template('restaurant_home.html',restaurant=username[0],menus=MENU)
        else:
            return render_template('login.html',"Incorrect User Type")
        account = c.fetchone()
        conn.commit()
        if account:
            session['loggedin'] = True

            return render_template('user_home.html',restaurants=RESTAURANT)
        else:
            return render_template('login.html',msg= "Incorrect Phone Number/Password")
    return render_template('login.html')

#Register Page
@app.route('/register', methods =['GET', 'POST'])
def register():
    if request.method=='POST' and 'user_type' in request.form and 'name' in request.form and 'phone' in request.form and 'street' in request.form and 'city' in request.form and 'state' in request.form and 'pincode' in request.form and 'email' in request.form and 'password' in request.form and 'confirm_password' in request.form:     
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
        if password == confirm_password:
            if user_type == 'Customer':
                c.execute("INSERT INTO customers VALUES (NULL,?,?,?,?,?,?,?,?)",(name,phone,street,city,state,pincode,email,password))
            elif user_type == 'Restaurant':
                c.execute("INSERT INTO restaurants VALUES (NULL,?,?,?,?,?,?,?,?)",(name,phone,street,city,state,pincode,email,password))
        else:
            return render_template('register.html',msg="Both Passwords do not match")
        conn.commit()
        return render_template('login.html')
    return render_template('register.html')

#User Home Page
@app.route('/user_home',methods=['GET','POST'])
def user_home():
    if request.method == 'POST' :
        return render_template('login.html')   
    return render_template('user_home.html',restaurants=RESTAURANT)
#Restaurant Home Page
@app.route('/restaurant_home',methods=['GET','POST'])
def restaurant_home():
    if request.method == 'POST':
        pass
    return render_template('restaurant_home.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return render_template('login.html')

if __name__== '__main__':
    app.run(host='0.0.0.0',debug=True)
