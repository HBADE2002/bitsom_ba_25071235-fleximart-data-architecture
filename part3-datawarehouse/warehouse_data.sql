INSERT INTO dim_date VALUES
(20240101,'2024-01-01','Monday',1,1,'January','Q1',2024,false),
(20240102,'2024-01-02','Tuesday',2,1,'January','Q1',2024,false),
(20240103,'2024-01-03','Wednesday',3,1,'January','Q1',2024,false),
(20240104,'2024-01-04','Thursday',4,1,'January','Q1',2024,false),
(20240105,'2024-01-05','Friday',5,1,'January','Q1',2024,false),
(20240106,'2024-01-06','Saturday',6,1,'January','Q1',2024,true),
(20240107,'2024-01-07','Sunday',7,1,'January','Q1',2024,true),
(20240110,'2024-01-10','Wednesday',10,1,'January','Q1',2024,false),
(20240113,'2024-01-13','Saturday',13,1,'January','Q1',2024,true),
(20240114,'2024-01-14','Sunday',14,1,'January','Q1',2024,true),
(20240115,'2024-01-15','Monday',15,1,'January','Q1',2024,false),
(20240120,'2024-01-20','Saturday',20,1,'January','Q1',2024,true),
(20240121,'2024-01-21','Sunday',21,1,'January','Q1',2024,true),
(20240125,'2024-01-25','Thursday',25,1,'January','Q1',2024,false),
(20240131,'2024-01-31','Wednesday',31,1,'January','Q1',2024,false),

(20240201,'2024-02-01','Thursday',1,2,'February','Q1',2024,false),
(20240202,'2024-02-02','Friday',2,2,'February','Q1',2024,false),
(20240203,'2024-02-03','Saturday',3,2,'February','Q1',2024,true),
(20240204,'2024-02-04','Sunday',4,2,'February','Q1',2024,true),
(20240205,'2024-02-05','Monday',5,2,'February','Q1',2024,false),
(20240210,'2024-02-10','Saturday',10,2,'February','Q1',2024,true),
(20240211,'2024-02-11','Sunday',11,2,'February','Q1',2024,true),
(20240214,'2024-02-14','Wednesday',14,2,'February','Q1',2024,false),
(20240215,'2024-02-15','Thursday',15,2,'February','Q1',2024,false),
(20240217,'2024-02-17','Saturday',17,2,'February','Q1',2024,true),
(20240218,'2024-02-18','Sunday',18,2,'February','Q1',2024,true),
(20240220,'2024-02-20','Tuesday',20,2,'February','Q1',2024,false),
(20240225,'2024-02-25','Sunday',25,2,'February','Q1',2024,true),
(20240228,'2024-02-28','Wednesday',28,2,'February','Q1',2024,false);

INSERT INTO dim_date VALUES
(20240229,'2024-02-29','Thursday',29,3,'March','Q1',2024,false);



INSERT INTO dim_product (product_id, product_name, category, subcategory, unit_price) VALUES
('P001','iPhone 14','Electronics','Mobile',69999),
('P002','Samsung Galaxy S21','Electronics','Mobile',45999),
('P003','Dell Laptop','Electronics','Laptop',79999),
('P004','Bluetooth Speaker','Electronics','Audio',4999),
('P005','LED TV 43 inch','Electronics','Television',32999),

('P006','Nike Shoes','Fashion','Footwear',3499),
('P007','Adidas T-Shirt','Fashion','Clothing',1299),
('P008','Levi Jeans','Fashion','Clothing',2999),
('P009','Puma Jacket','Fashion','Outerwear',5499),
('P010','Formal Shirt','Fashion','Clothing',1999),

('P011','Basmati Rice','Groceries','Grains',650),
('P012','Cooking Oil','Groceries','Essentials',1200),
('P013','Organic Honey','Groceries','Food',450),
('P014','Dry Fruits Pack','Groceries','Snacks',899),
('P015','Tea Powder','Groceries','Beverages',350);


INSERT INTO dim_customer (customer_id, customer_name, city, state, customer_segment) VALUES
('C001','Rahul Sharma','Mumbai','Maharashtra','Retail'),
('C002','Priya Patel','Ahmedabad','Gujarat','Retail'),
('C003','Amit Kumar','Delhi','Delhi','Corporate'),
('C004','Sneha Reddy','Hyderabad','Telangana','Retail'),
('C005','Vikram Singh','Mumbai','Maharashtra','Premium'),
('C006','Anjali Mehta','Ahmedabad','Gujarat','Retail'),
('C007','Ravi Verma','Delhi','Delhi','Corporate'),
('C008','Pooja Iyer','Hyderabad','Telangana','Retail'),
('C009','Karthik Nair','Mumbai','Maharashtra','Premium'),
('C010','Neha Shah','Ahmedabad','Gujarat','Retail'),
('C011','Arjun Rao','Delhi','Delhi','Corporate'),
('C012','Meera Nambiar','Hyderabad','Telangana','Premium');


INSERT INTO fact_sales
(date_key, product_key, customer_key, quantity_sold, unit_price, discount_amount, total_amount)
VALUES
(20240106,1,1,1,69999,2000,67999),
(20240107,2,2,2,45999,3000,88998),
(20240113,3,3,1,79999,0,79999),
(20240114,4,4,3,4999,500,14497),
(20240120,5,5,1,32999,1000,31999),
(20240121,6,6,2,3499,0,6998),
(20240125,7,7,4,1299,200,4996),
(20240131,8,8,1,2999,0,2999),

(20240203,9,9,2,5499,500,10498),
(20240204,10,10,3,1999,300,5697),
(20240210,11,11,5,650,0,3250),
(20240211,12,12,4,1200,200,4600),
(20240214,13,1,3,450,0,1350),
(20240215,14,2,2,899,0,1798),
(20240217,15,3,6,350,0,2100),

-- additional transactions to reach 40
(20240101,1,4,1,69999,0,69999),
(20240102,2,5,1,45999,1000,44999),
(20240103,3,6,1,79999,0,79999),
(20240104,4,7,2,4999,0,9998),
(20240105,5,8,1,32999,0,32999),
(20240110,6,9,3,3499,500,9997),
(20240115,7,10,2,1299,0,2598),
(20240121,8,11,2,2999,0,5998),
(20240125,9,12,1,5499,0,5499),
(20240131,10,1,3,1999,0,5997),

(20240201,11,2,5,650,0,3250),
(20240202,12,3,2,1200,0,2400),
(20240205,13,4,4,450,0,1800),
(20240210,14,5,2,899,0,1798),
(20240211,15,6,6,350,0,2100),
(20240218,1,7,1,69999,3000,66999),
(20240220,2,8,2,45999,2000,89998),
(20240225,3,9,1,79999,0,79999),
(20240228,4,10,3,4999,0,14997);


INSERT INTO fact_sales
(date_key, product_key, customer_key, quantity_sold, unit_price, discount_amount, total_amount)
VALUES
(20240225,14,5,2,899,0,1798),
(20240228,15,6,6,350,0,2100),
(20240218,1,7,1,69999,3000,66999),
(20240220,2,8,2,45999,2000,89998),
(20240217,3,9,1,79999,0,79999),
(20240214,4,10,3,4999,0,14997);


