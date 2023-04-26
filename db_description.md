# All the 5 tables are in 3 NF as there are no Many-to-Many relationships between any of the tables and each has a non prime primary keys.

# The Functional Dependencies:
Customers table:
CustomerId -> {CustomerName, Phone, Street, City, State, PinCode, Email, Password}
Restaurants table:
RestaurantId -> {RestaurantName, Phone, Street, City, State, Pincode, Email, Password, DeliveryFee}
Items table:
ItemId -> {RestaurantId, ItemName, Price, Description, PreparationTime}
RestaurantId -> {DeliveryFee}
Orders table:
OrderId -> {CustomerId, RestaurantId, OrderDate, Tax, Total}
CustomerId -> {CustomerName, Phone, Street, City, State, PinCode, Email, Password}
RestaurantId -> {RestaurantName, Phone, Street, City, State, Pincode, Email, Password, DeliveryFee}
OrderDetails table:
OrderDetailsID -> {OrderId, ItemId}
OrderId -> {CustomerId, RestaurantId, OrderDate, Tax, Total}
ItemId -> {RestaurantId, ItemName, Price, Description, PreparationTime}
Cart table:
CartId -> {ItemId}
ItemId -> {RestaurantId, ItemName, Price, Description, PreparationTime}

# Customers Table
Customers(CustomerId,CustomerName,Phone,Street,City,State,PinCode,Email,Password)
The Customer table stores CustomerId which is auto generated in increments, CustomerName, Phone Number, Address(Street, State, Pincode), E-Mail,Password
The table has Primary Key CustomerId, and no Foreign Key so no triggers or policies are needed.

# Sample Data for Customers:
1	Yugi	98765	2330 	Wichita	Kansas	67220	yugi@anymail.com	98765
2	Sunny	98764	2156	Wichita	Kansas	67220	sunny@anymail.com	98764

# Restaurants Table 
Restaurants(RestaurantId,RestaurantName,Phone,Street,City,State,Pincode,Email,Password,DeliveryFee)
The Restaurant table stores RestaurantId which is auto generated in increments, Restaurant Name, Phone Number, Address(Street, State, Pincode),Password, Delivery Fee.
The table has Primary Key RestaurantId, and no Foreign Key so no triggers or policies are needed.

# Sample Data for Restaurants:
RestaurantId	RestaurantName	Phone	Street	City	State	Pincode	Email	Password
1	Bean Machine	12345	2330	Wichita	Kansas	67220	beanmachine@anymail.com	12345
2	Cluckin Bell	12346	2330	Wichita	Kansas	67220	cluckinbell@anymail.com	12346
3	Taco Bomb	12347	2126	Wichita	Kansas	67221	tacobomb@anymail.com	12347

# Items Table
Items(ItemId,RestaurantId,ItemName,Price,Description,PreparationTime)
The Items table stores ItemId which is auto generated in increments, RestaurantId, Item Name, Price of the item, Description of the item, Preparation Time of the item.
The table has ItemId Primary key and RestaurantId as foreign key that references to Restaurants Table.
 If the referenced restaurant does not exist, the trigger raises an error and roll back the transaction. In our website the Items entry could be done only from the restaurant page which ensures the restaurant is present before creating the item. Same applies for the policy

# Sample Data for Items:
1	1	Medium Caramel Cold Coffee	6.99	Espresso, Milk, Caramel, Ice Cubes	3
6	1	Medium Caramel Hot Coffee	7.49	Espresso, Milk, Caramel	4
7	1	Large Caramel Hot Coffee	8.99	Espresso, Milk, Caramel	4

# Orders Table
Orders(OrderId,CustomerId,RestaurantId,OrderDate,Tax,Total)
The Orders table stores OrderId which is auto-generated, CustomerId, RestaurantId, Order Date, Tax and the order total.
The OrderId is the primary key and foreign keys CustomerId references to Customers table, RestaurantId to Restaurants table. 
The trigger here is if the referenced customer or restaurant doesn't exist the order is not created. Same for the policy.
In our case, the orders table is updated from the website only when a user selects the restaurant and choses the item to be added to the cart and when cart is confirmed, only then the order is created otherwise the order is not created.

# Sample data for orders
 5	9	8	2023-04-25 21:10:49	0.349	10.329
4	7	7	2023-04-25 20:45:57	0.3735	11.094

# OrderDetails Table
OrderDetails(OrderDetailsID,OrderId,ItemId)
This stores OrderId and ItemId. This is created to break Many to many relation betweeen Orders and Items Tables.
Here OrderDetailsId is the primary key and OrderId, ITemId are foreign keys.
The Trigger here is the item id and order id are added to the table only when they exist in their respective tables.
This is ensured by updating the OrderDetails table only when an order is finalized.

# Sample data for OrderDetails 
1	1	1
2	1	7

# Cart Table
Cart(CartId,ItemId)
The Cart is used to temporarily hold the item details before an order is placed. Once the order is placed Cart table is cleared.
The trigger here is the item is added to the cart only when it exists in Item Table.
The Primary Key is CartId, and foreign key ItemId references to Items Table.
