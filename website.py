from flask import Flask,render_template,request, redirect, url_for,session
from datetime import datetime
import sqlite3

app=Flask(__name__,static_url_path='/static')
app.secret_key='123456789'
conn = sqlite3.connect('website_data.db',check_same_thread=False)
c = conn.cursor()

#Create Database Tables if they do not exist
#Create customers Table
c.execute('''CREATE TABLE IF NOT EXISTS Customers (CustomerId INTEGER PRIMARY KEY AUTOINCREMENT, CustomerName VARCHAR(100),Phone VARCHAR(10),Street VARCHAR(50),City VARHCAR(50),State VARCHAR(50),Pincode INTEGER,Email VARCHAR(50),Password VARCHAR(15))''')

#Create retaurants table
c.execute('''CREATE TABLE IF NOT EXISTS Restaurants (RestaurantId INTEGER PRIMARY KEY AUTOINCREMENT, RestaurantName VARCHAR(100),Phone VARCHAR(10),Street VARCHAR(50),City VARHCAR(50),State VARCHAR(50),Pincode INTEGER,Email VARCHAR(50),Password VARCHAR(15),DeliveryFee INTEGER)''')
conn.commit()

#Create items table
c.execute('''CREATE TABLE IF NOT EXISTS Items(ItemId INTEGER PRIMARY KEY AUTOINCREMENT,RestaurantId INTEGER,ItemName VARCHAR(100),Price INTEGER,Contents VARCHAR(200),PreparationTime INTEGER,FOREIGN KEY (RestaurantId) REFERENCES restaurants(RestaurantId) ON DELETE CASCADE)''')
conn.commit()

#Create orders table
c.execute('''CREATE TABLE IF NOT EXISTS Orders(OrderId INTEGER PRIMARY KEY AUTOINCREMENT,CustomerId INTEGER,RestaurantId INTEGER,OrderDate DATE,Tax INTEGER,Total INTEGER,FOREIGN KEY (CustomerId) REFERENCES Customers(CustomerId) ON DELETE CASCADE,FOREIGN KEY (RestaurantId) REFERENCES Restaurants(RestaurantId) ON DELETE CASCADE)''')
conn.commit()

#Create Order Details table
c.execute('''CREATE TABLE IF NOT EXISTS OrderDetails(OrderDetailsID INTEGER PRIMARY KEY AUTOINCREMENT,OrderId INTEGER,ItemId INTEGER,FOREIGN KEY (OrderId) REFERENCES Orders(OrderId) ON DELETE CASCADE,FOREIGN KEY (ItemId) REFERENCES Items(ItemId) ON DELETE CASCADE)''')
conn.commit()

#Create carts table
c.execute('''CREATE TABLE IF NOT EXISTS Cart(CartId INTEGER PRIMARY KEY AUTOINCREMENT,ItemId INTEGER,FOREIGN KEY (ItemId) REFERENCES Items(ItemId) ON DELETE CASCADE)''')
conn.commit()

#SQL Commands
CUSTOMER_INFO="SELECT * FROM Customers WHERE Phone = ? AND Password = ?"
RESTAURANT_INFO="SELECT * FROM Restaurants WHERE Phone = ? AND Password = ?"
REGISTER_CUSTOMER_ENTRY="INSERT INTO Customers VALUES (NULL,?,?,?,?,?,?,?,?)"
REGISTER_RESTAURANT_ENTRY="INSERT INTO Restaurants VALUES (NULL,?,?,?,?,?,?,?,?,?)"
CUSTOMER_DETAILS_BY_CUSTID="SELECT * FROM Customers WHERE CustomerId=?"
RESTAURANT_DETAILS_BY_RESTID="SELECT * FROM Items WHERE RestaurantId=?"
ADD_MENU_ITEM="INSERT INTO Items VALUES(NULL,?,?,?,?,?)"
DELETE_MENU_ITEM="DELETE FROM Items where ItemId=?"
GET_REST_NAME="SELECT RestaurantName FROM Resaurants WHERE RestaurantId=?"
GET_CUST_NAME="SELECT CustomerName FROM Customers WHERE CustomerId=?"
GET_DELIVERY_FEE="SELECT DeliveryFee FROM Restaurants WHERE RestaurantId=?"
GET_ITEMS_BY_RESTID="SELECT * FROM Items WHERE RestaurantId=?"
GET_ITEMS_BY_ITEMID="SELECT Price from Items where ItemId=?"
ADD_ITEMS_TO_CART="INSERT INTO Cart VALUES(NULL,?)"
DISPLAY_CART_ITEMS="SELECT ROW_NUMBER() OVER(ORDER BY Items.ItemId),Items.ItemName, Items.Price FROM Items INNER JOIN Cart ON Items.ItemId = Cart.ItemId"
CART_TOTAL="SELECT SUM(Items.Price) FROM Items INNER JOIN Cart ON Items.ItemId = Cart.ItemId"
GET_CART_ITEMID ="SELECT ItemId FROM Cart"
ADD_TO_ORDER="INSERT INTO Orders VALUES(NULL,?,?,?,?,?)"
ADD_TO_ORDER_DETAILS="INSERT INTO OrderDetails VALUES(NULL,?,?)"
GET_LATEST_ORDER="SELECT OrderId, Total,OrderDate FROM Orders ORDER BY OrderDate DESC LIMIT 1"
DELETE_CART_ITEMS="DELETE FROM Cart"
VIEW_REST_ORDERS="SELECT o.OrderId, r.RestaurantName, r.Phone, group_concat(i.ItemName, ', '), o.Total FROM Orders o INNER JOIN Restaurants r ON o.RestaurantId = r.RestaurantId INNER JOIN OrderDetails od ON o.OrderId = od.OrderId INNER JOIN Items i ON od.ItemId = i.ItemId WHERE o.CustomerId = ? GROUP BY o.OrderId"
VIEW_CUSTOMER_ORDERS="SELECT o.OrderId, c.CustomerName, c.Phone, group_concat(i.ItemName, ', ') as OrderItems, o.Total FROM Orders o INNER JOIN Customers c ON o.CustomerId = c.CustomerId INNER JOIN OrderDetails od ON o.OrderId = od.OrderId INNER JOIN Items i ON od.ItemId = i.ItemId WHERE o.RestaurantId = ? GROUP BY o.OrderId"
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
            c.execute(CUSTOMER_INFO, (phone, password))
        #Get Restaurant Name if Restaurant is logging in
        else:
            c.execute(RESTAURANT_INFO, (phone, password))
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
                c.execute(REGISTER_CUSTOMER_ENTRY,(name,phone,street,city,state,pincode,email,password))
            #If user_type is Restaurant add info to restarurants table
            else:
                if delivery_fee:
                    c.execute(REGISTER_RESTAURANT_ENTRY,(name,phone,street,city,state,pincode,email,password,delivery_fee))
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
    c.execute(CUSTOMER_DETAILS_BY_CUSTID,(CustId,))
    conn.commit()
    user=c.fetchone()
    c.execute("SELECT * FROM restaurants WHERE Pincode=?",(user[6],))
    conn.commit()
    restaurants=c.fetchall()
    if request.method == 'POST'and request.form['action']=='Order':
        RestId=request.form['RestId'] 
        RestName=request.form['RestName']
        session['RestId']=RestId
        session['RestName']=RestName
        return redirect('/menu')
    elif request.method == 'POST' and request.form['action'] == 'View Orders':
        return redirect('/customer_view_orders')
    elif request.method == 'POST'and request.form['action']=='logout':
        return redirect('/logout')
    return render_template('user_home.html',profile=user[1],restaurants=restaurants)

#Restaurant Home Page
@app.route('/restaurant_home',methods=['POST','GET'])
def restaurant_home():
    RestId=session['RestId']
    c.execute(RESTAURANT_DETAILS_BY_RESTID,(RestId,))
    conn.commit()
    menus=c.fetchall()
    if request.method == 'POST' and request.form['action'] == 'Add':
        ItemName=request.form['name']
        ItemContents=request.form['contents']
        ItemPrice=request.form['price']
        PrepTime=request.form['preparation_time']
        try:
            c.execute(ADD_MENU_ITEM,(RestId,ItemName,ItemPrice,ItemContents,PrepTime))
            conn.commit()
            return redirect('/restaurant_home')
        except: 'There was an issue adding your item'
        return redirect('/restaurant_home')
    elif request.method == 'POST' and request.form['action'] == 'Remove':
        itemId = request.form['MenuId']
        try:
            c.execute(DELETE_MENU_ITEM,itemId)
            conn.commit()
            return redirect('/restaurant_home')
        except: 'There was an issue removing your item'
        return redirect('/restaurant_home')
    elif request.method == 'POST' and request.form['action'] == 'View Orders':
        return redirect('/restaurant_view_orders')
    elif request.method == 'POST'and request.form['action']=='logout':
        return redirect('/logout')
    return render_template('restaurant_home.html',restaurant=session['username'],menus=menus)

#Route for Menu
@app.route('/menu',methods=['POST','GET'])
def menu():
    RestId=session['RestId']
    RestName=session['RestName']
    UserId=session['UserId']
    c.execute(GET_ITEMS_BY_RESTID,(RestId,))
    conn.commit()
    items=c.fetchall()  
    if request.method == 'POST' and request.form['action'] == 'Add to Cart':
        ItemId=request.form['ItemId']
        Price=c.fetchone()
        c.execute(ADD_ITEMS_TO_CART,(ItemId,))
        conn.commit()
        return redirect('/menu')
    elif request.method == 'POST' and request.form['action'] == 'Go to Cart':
        return redirect('/cart')
    elif request.method == 'POST' and request.form['action'] == 'View Orders':
        return redirect('/customer_view_orders')
    return render_template('menu.html',restaurant=RestName,items=items)

#cart route
@app.route('/cart',methods=['POST','GET'])
def cart():
    c.execute(DISPLAY_CART_ITEMS)
    conn.commit()
    cartItems=c.fetchall()
    c.execute(CART_TOTAL)
    conn.commit()
    total=c.fetchone()
    tax=0.05
    c.execute(GET_DELIVERY_FEE,(session['RestId'],))
    conn.commit()
    deliveryFee=c.fetchone()
    Ordertotal=total[0]
    if Ordertotal is None:
        Ordertotal=0
        tax=0
    else:
        tax=round(Ordertotal*0.05,3)
    Ordertotal=round(Ordertotal+tax+deliveryFee[0],3)

    if request.method == 'POST' and request.form['action']=='logout':
        return redirect('logout')
    elif request.method == 'POST' and request.form['action']=='Place Order':
        c.execute(CART_TOTAL)
        Total=c.fetchone()
        conn.commit()
        c.execute(GET_DELIVERY_FEE,(session['RestId'],))
        conn.commit()
        deliveryFee=c.fetchone()
        Tax=Total[0]*0.05
        OrderTotal=round(Total[0]+Tax+deliveryFee[0],3)
        date_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute(ADD_TO_ORDER,(session['UserId'],session['RestId'],date_created,Tax,OrderTotal,))
        conn.commit()
        c.execute(GET_LATEST_ORDER)
        conn.commit()
        OrderId=c.fetchone()
        c.execute(GET_CART_ITEMID)
        conn.commit()
        ItemIds=c.fetchall()
        for ItemId in ItemIds:
            c.execute(ADD_TO_ORDER_DETAILS,(OrderId[0],ItemId[0]))
            conn.commit()
        return redirect('/order_placed')
    return render_template('cart.html',items=cartItems,restaurant=session['RestName'],total=Ordertotal,tax=tax,deliveryFee=deliveryFee[0])

#Place Order Route
@app.route('/order_placed',methods=['POST','GET'])
def order_placed():
    c.execute(DELETE_CART_ITEMS)
    conn.commit()
    if request.method == 'POST' and request.form['action'] == 'logout':
        return redirect('/logout')
    c.execute(GET_LATEST_ORDER)
    conn.commit()
    OrderInfo=c.fetchall()
    print(OrderInfo)
    return render_template("order_placed.html",OrderId=OrderInfo[0][0],total=OrderInfo[0][1],OrderDate=OrderInfo[0][2])

#Restaurant View Orders Route
@app.route('/restaurant_view_orders',methods=['POST','GET'])
def restaurant_view_orders():
    c.execute(VIEW_CUSTOMER_ORDERS,(session['RestId'],))
    conn.commit()
    orders=c.fetchall()
    print(orders)
    if request.method == 'POST' and request.form['action'] =='logout':
        return redirect("/logout")
    return render_template("/view_orders.html",profile=session['RestName'],orders=orders)

#Customer View Orders Route
@app.route('/customer_view_orders',methods=['POST','GET'])
def customer_view_orders():
    c.execute(VIEW_REST_ORDERS,(session['UserId'],))
    conn.commit()
    orders=c.fetchall()
    c.execute(GET_CUST_NAME,(session['UserId'],))
    conn.commit()
    CustName=c.fetchone()
    if request.method == 'POST' and request.form['action'] =='logout':
        return redirect("/logout")
    return render_template("view_orders.html",profile=CustName[0],orders=orders)

#logout route
@app.route('/logout',methods=['POST','GET'])
def logout():
    c.execute(DELETE_CART_ITEMS)
    conn.commit()
    session.pop('logged_in', None)
    return render_template('login.html')

if __name__== '__main__':
    app.run(host='0.0.0.0',debug=True)
