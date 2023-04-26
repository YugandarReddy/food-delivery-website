# Read Data from Customers Table
SELECT * FROM Customers WHERE Phone = 123 AND Password = 123"

SELECT CustomerName FROM Customers WHERE CustomerId=1;

SELECT * FROM Customers WHERE CustomerId=1;

SELECT CustomerName FROM Customers WHERE CustomerId=1;

# Read Data from Restaurants Table
SELECT RestaurantName FROM Resaurants WHERE RestaurantId=2;

SELECT DeliveryFee FROM Restaurants WHERE RestaurantId=2;

SELECT * FROM Restaurants WHERE Phone = 123 AND Password = 123";



# Read Data from Items Table
SELECT Price from Items where ItemId=3;

SELECT * FROM Items WHERE RestaurantId=2";

SELECT Price from Items where ItemId=3";

SELECT SUM(Items.Price) 
FROM Items INNER 
JOIN Cart 
ON Items.ItemId = Cart.ItemId";


# Read Data from Orders Table
SELECT o.OrderId, r.RestaurantName, r.Phone, group_concat(i.ItemName, ', '), o.Total 
FROM Orders o 
INNER JOIN Restaurants r 
ON o.RestaurantId = r.RestaurantId 
INNER JOIN OrderDetails od 
ON o.OrderId = od.OrderId 
INNER JOIN Items i 
ON od.ItemId = i.ItemId 
WHERE o.CustomerId = 3 
GROUP BY o.OrderId";

SELECT o.OrderId, c.CustomerName, c.Phone, group_concat(i.ItemName, ', ') as OrderItems, o.Total 
FROM Orders o 
INNER JOIN Customers c
ON o.CustomerId = c.CustomerId 
INNER JOIN OrderDetails od 
ON o.OrderId = od.OrderId 
INNER JOIN Items i 
ON od.ItemId = i.ItemId 
WHERE o.RestaurantId = 3 
GROUP BY o.OrderId";

SELECT OrderId, Total,OrderDate 
FROM Orders 
ORDER BY OrderDate DESC LIMIT 1;


# Read Data from Cart Table
SELECT ROW_NUMBER() OVER(ORDER BY Items.ItemId),Items.ItemName, Items.Price 
FROM Items 
INNER JOIN Cart 
ON Items.ItemId = Cart.ItemId";

SELECT ItemId FROM Cart;

# Delete Data from Cart Table
DELETE FROM Cart;

# Delete item from Items table
DELETE FROM Items where ItemId=2;