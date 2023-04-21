from flask import Flask,render_template

app=Flask(__name__)
RESTAURANT=[{"RestaurantID":1,"Name":"Biryani House","DeliveryFee":5,"City":"Wichita","State":"Ks","PinCode":123455},{"RestaurantID":2,"Name":"Dosa Palace","DeliveryFee":3,"City":"Wichita","State":"Ks","PinCode":123455},{"RestaurantID":3,"Name":"Paradise","DeliveryFee":6,"City":"Wichita","State":"Ks","PinCode":123455},{"RestaurantID":4,"Name":"Bawarchi","DeliveryFee":3,"City":"Wichita","State":"Ks","PinCode":123457}]
MENU=[{"ItemID":1,"Name":"Biryani","Price":15,"Preparation_Time":20,"Description":"Rice Flavoured with Indian Spices"},{"ItemID":2,"Name":"Idli","Price":10,"Preparation_Time":10,"Description":"Steam cooked pan cake batter with dip of tomato chutney"},{"ItemID":3,"Name":"Dosa","Price":5,"Preparation_Time":7,"Description":"pan cake batter with dip of coconut chutney"},{"ItemID":4,"Name":"Tandoori Chicken","Price":15,"Preparation_Time":20,"Description":"Chicken roasted in Tandoor"},{"ItemID":5,"Name":"Grill Chicken","Price":15,"Preparation_Time":20,"Description":"Chicken Grilled on Charcoal"}]
@app.route("/")
def login_page():
    return render_template('Restaurant_List.html',restaurants=RESTAURANT)

if __name__== '__main__':
    app.run(host='0.0.0.0',debug=True)