from flask import Flask,render_template,request, redirect, url_for,session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
'''
conn = sqlite3.connect('food_delivery.db')
c = conn.cursor()
'''
'''
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(200), nullable=False)
    street = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(200), nullable=False)
    state = db.Column(db.String(200), nullable=False)
    pincode = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr(self):
        return '<Customer %r>' % self.name
'''
'''
RESTAURANT=[{"RestaurantID":1,"Name":"Biryani House","DeliveryFee":5,"City":"Wichita","State":"Ks","PinCode":123455},{"RestaurantID":2,"Name":"Dosa Palace","DeliveryFee":3,"City":"Wichita","State":"Ks","PinCode":123455},{"RestaurantID":3,"Name":"Paradise","DeliveryFee":6,"City":"Wichita","State":"Ks","PinCode":123455},{"RestaurantID":4,"Name":"Bawarchi","DeliveryFee":3,"City":"Wichita","State":"Ks","PinCode":123457}]
MENU=[{"ItemID":1,"Name":"Biryani","Price":15,"Preparation_Time":20,"Description":"Rice Flavoured with Indian Spices"},{"ItemID":2,"Name":"Idli","Price":10,"Preparation_Time":10,"Description":"Steam cooked pan cake batter with dip of tomato chutney"},{"ItemID":3,"Name":"Dosa","Price":5,"Preparation_Time":7,"Description":"pan cake batter with dip of coconut chutney"},{"ItemID":4,"Name":"Tandoori Chicken","Price":15,"Preparation_Time":20,"Description":"Chicken roasted in Tandoor"},{"ItemID":5,"Name":"Grill Chicken","Price":15,"Preparation_Time":20,"Description":"Chicken Grilled on Charcoal"}]
'''

#Login Page
@app.route("/")
@app.route("/login",methods=['POST','GET'])
def login():
    if request.method=='POST' and 'username' in request.form and 'password' in request.form:
        phone = request.form['username']
        password = request.form['password']
    return render_template('login.html')
    '''
        Connect database to check for user
        c.execute("SELECT * FROM accounts WHERE phone = % s AND password = % s", (phone, password))'
        account = c.fetchone()
        conn.commit()
        
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            return render_template('index.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
'''

@app.route('/register', methods =['GET', 'POST'])
def register():
    if request.method=='POST' :
         return render_template('login.html')   
    return render_template('register.html')

@app.route('/restaurant_list',methods=['GET','POST'])
def restaurant_list():
    if request.method=='POST' :
         return render_template('login.html')   
    return render_template('restaurant_list.html')


if __name__== '__main__':
    app.run(host='0.0.0.0',debug=True)
