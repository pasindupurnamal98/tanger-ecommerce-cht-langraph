-- SQL Server Database Setup Script for Singer E-commerce Customer Support Chatbot
-- This script creates the database schema and inserts sample data.

-- Create Database (if not exists)
-- USE master;
-- GO
-- IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = N'SingerEcommerceDB')
-- BEGIN
--     CREATE DATABASE SingerEcommerceDB;
-- END
-- GO

-- USE SingerEcommerceDB;
-- GO

-- Drop tables if they exist (to allow re-running the script)
IF OBJECT_ID('Warranties', 'U') IS NOT NULL DROP TABLE Warranties;
IF OBJECT_ID('OrderItems', 'U') IS NOT NULL DROP TABLE OrderItems;
IF OBJECT_ID('Orders', 'U') IS NOT NULL DROP TABLE Orders;
IF OBJECT_ID('SpareParts', 'U') IS NOT NULL DROP TABLE SpareParts;
IF OBJECT_ID('Products', 'U') IS NOT NULL DROP TABLE Products;
IF OBJECT_ID('Categories', 'U') IS NOT NULL DROP TABLE Categories;
IF OBJECT_ID('Users', 'U') IS NOT NULL DROP TABLE Users;
IF OBJECT_ID('Stores', 'U') IS NOT NULL DROP TABLE Stores;
GO




-- Schema Creation



CREATE TABLE Users (
    UserID INT PRIMARY KEY IDENTITY(1,1),
    Name NVARCHAR(100),
    Email NVARCHAR(100),
    Phone NVARCHAR(20),
    Address NVARCHAR(255)
);

CREATE TABLE Categories (
    CategoryID INT PRIMARY KEY IDENTITY(1,1),
    Name NVARCHAR(50),
    Description NVARCHAR(255)
);

CREATE TABLE Products (
    ProductID INT PRIMARY KEY IDENTITY(1,1),
    Name NVARCHAR(100),
    CategoryID INT FOREIGN KEY REFERENCES Categories(CategoryID),
    Description NVARCHAR(255),
    Price DECIMAL(10, 2),
    Stock INT
);

CREATE TABLE Orders (
    OrderID INT PRIMARY KEY IDENTITY(1,1),
    UserID INT FOREIGN KEY REFERENCES Users(UserID),
    OrderDate DATETIME,
    Status NVARCHAR(50),
    DeliveryDate DATETIME
);

CREATE TABLE OrderItems (
    OrderItemID INT PRIMARY KEY IDENTITY(1,1),
    OrderID INT FOREIGN KEY REFERENCES Orders(OrderID),
    ProductID INT FOREIGN KEY REFERENCES Products(ProductID),
    Quantity INT,
    Price DECIMAL(10, 2)
);

CREATE TABLE Warranties (
    WarrantyID INT PRIMARY KEY IDENTITY(1,1),
    OrderItemID INT FOREIGN KEY REFERENCES OrderItems(OrderItemID),
    StartDate DATETIME,
    EndDate DATETIME
);

CREATE TABLE SpareParts (
    PartID INT PRIMARY KEY IDENTITY(1,1),
    ProductID INT FOREIGN KEY REFERENCES Products(ProductID),
    PartName NVARCHAR(100),
    Stock INT,
    Price DECIMAL(10, 2)
);

CREATE TABLE Stores (
    StoreID INT PRIMARY KEY IDENTITY(1,1),
    Name NVARCHAR(100),
    Address NVARCHAR(255),
    Phone NVARCHAR(20),
    City NVARCHAR(50)
);
GO




-- Sample Data Insertion


SET IDENTITY_INSERT Users ON;
SET IDENTITY_INSERT Users OFF;

INSERT INTO Users (UserID, Name, Email, Phone, Address) VALUES (1, N'Alice Smith', N'alice.smith@example.com', N'0771234567', N'123 Main St, Colombo');
INSERT INTO Users (UserID, Name, Email, Phone, Address) VALUES (2, N'Bob Johnson', N'bob.j@example.com', N'0719876543', N'456 High St, Kandy');
INSERT INTO Users (UserID, Name, Email, Phone, Address) VALUES (3, N'Catherine Lee', N'cathy.l@example.com', N'0765432109', N'789 Oak Ave, Galle');
INSERT INTO Users (UserID, Name, Email, Phone, Address) VALUES (4, N'David Chen', N'david.c@example.com', N'0701122334', N'101 Pine Rd, Jaffna');
INSERT INTO Users (UserID, Name, Email, Phone, Address) VALUES (5, N'Eva Green', N'eva.g@example.com', N'0758899001', N'202 Elm St, Negombo');

SET IDENTITY_INSERT Categories OFF;

INSERT INTO Categories (CategoryID, Name, Description) VALUES (1, N'Mobiles & Tablets, Computers, Printers, Gadgets & Accessories', N'Electronics and IT related products');
INSERT INTO Categories (CategoryID, Name, Description) VALUES (2, N'Home Appliances', N'Appliances for home use');
INSERT INTO Categories (CategoryID, Name, Description) VALUES (3, N'Kitchen Appliances', N'Appliances for kitchen use');
INSERT INTO Categories (CategoryID, Name, Description) VALUES (4, N'TV, Home Audio Video & Smart Boards', N'Entertainment and smart home devices');
INSERT INTO Categories (CategoryID, Name, Description) VALUES (5, N'Refrigerators, Air Conditioners, Washing Machines, Freezers & Coolers', N'Large cooling and washing appliances');
INSERT INTO Categories (CategoryID, Name, Description) VALUES (6, N'Furniture', N'Home and office furniture');
INSERT INTO Categories (CategoryID, Name, Description) VALUES (7, N'Personal Care & Fitness Equipment', N'Health, beauty and fitness products');
INSERT INTO Categories (CategoryID, Name, Description) VALUES (8, N'Fans', N'Various types of fans');
INSERT INTO Categories (CategoryID, Name, Description) VALUES (9, N'Air Coolers', N'Air cooling devices');
INSERT INTO Categories (CategoryID, Name, Description) VALUES (10, N'Scales', N'Weighing scales');
INSERT INTO Categories (CategoryID, Name, Description) VALUES (11, N'Lighting Products', N'Lighting solutions');
INSERT INTO Categories (CategoryID, Name, Description) VALUES (12, N'Water Filters, Purifiers & Geysers', N'Water treatment and heating devices');
INSERT INTO Categories (CategoryID, Name, Description) VALUES (13, N'Vacuum Cleaners', N'Cleaning appliances');
INSERT INTO Categories (CategoryID, Name, Description) VALUES (14, N'Irons', N'Garment care irons');
INSERT INTO Categories (CategoryID, Name, Description) VALUES (15, N'Air Purifiers', N'Air purification devices');
INSERT INTO Categories (CategoryID, Name, Description) VALUES (16, N'Floor Cleaners', N'Floor cleaning machines');
INSERT INTO Categories (CategoryID, Name, Description) VALUES (17, N'Floor Polishers', N'Floor polishing machines');
INSERT INTO Categories (CategoryID, Name, Description) VALUES (18, N'Garden Equipment', N'Tools for garden maintenance');
INSERT INTO Categories (CategoryID, Name, Description) VALUES (19, N'High Pressure Cleaners', N'High pressure cleaning devices');
INSERT INTO Categories (CategoryID, Name, Description) VALUES (20, N'Sewing Machines, Sewing Courses & Learning Solutions', N'Sewing related products and services');
INSERT INTO Categories (CategoryID, Name, Description) VALUES (21, N'Agro Products', N'Agricultural products');
INSERT INTO Categories (CategoryID, Name, Description) VALUES (22, N'Other Products', N'Miscellaneous products');

SET IDENTITY_INSERT Products ON;


INSERT INTO Products (ProductID, Name, CategoryID, Description, Price, Stock) VALUES (1, N'Sisil Inverter Refrigerator SL-INV-285H', 5, N'No Frost, 285L', 149999.00, 10);
INSERT INTO Products (ProductID, Name, CategoryID, Description, Price, Stock) VALUES (2, N'Singer Hand Mixer KA-HM-01', 3, N'360W, 5 Speeds', 7694.00, 50);
INSERT INTO Products (ProductID, Name, CategoryID, Description, Price, Stock) VALUES (3, N'Singer Kitchen Machine 5L, 1400W', 3, N'5L, 1400W', 34199.00, 20);
INSERT INTO Products (ProductID, Name, CategoryID, Description, Price, Stock) VALUES (4, N'Panasonic 43" 4K Smart Google TV', 4, N'TH-43PX740N', 144999.00, 15);
INSERT INTO Products (ProductID, Name, CategoryID, Description, Price, Stock) VALUES (5, N'Honor 200 Smart 5G', 1, N'8GB / 256GB, White', 69999.00, 30);
INSERT INTO Products (ProductID, Name, CategoryID, Description, Price, Stock) VALUES (6, N'ASUS Vivobook 15', 1, N'X1504VA-NJ7656WS, 13th Intel', 299999.00, 5);
INSERT INTO Products (ProductID, Name, CategoryID, Description, Price, Stock) VALUES (7, N'Singer Glass Top Fully Automatic Washing Machine', 5, N'SWM-FAR75GT', 81999.00, 12);
INSERT INTO Products (ProductID, Name, CategoryID, Description, Price, Stock) VALUES (8, N'Singer Air Conditioner - Smart WIFI Inverter', 5, N'SASI12INPRO', 214999.00, 8);
INSERT INTO Products (ProductID, Name, CategoryID, Description, Price, Stock) VALUES (9, N'Singer Air Conditioner - Non-Inverter 24000 BTU', 5, N'SAS24TCNRN', 279999.00, 7);
INSERT INTO Products (ProductID, Name, CategoryID, Description, Price, Stock) VALUES (10, N'Tefal Steam Irons Express Steam Plus FV2882G0', 14, N'2400W, Ceramic Soleplate', 27499.00, 40);
INSERT INTO Products (ProductID, Name, CategoryID, Description, Price, Stock) VALUES (11, N'KDK Ventilating Fan Ceiling Mount Duct Type', 8, N'150mm, 18W', 64900.00, 25);
INSERT INTO Products (ProductID, Name, CategoryID, Description, Price, Stock) VALUES (12, N'Hitachi Cordless Stick Vacuum Cleaner PV-X90N', 13, N'2-in-1, Lightweight', 77999.00, 18);

INSERT INTO Orders (OrderID, UserID, OrderDate, Status, DeliveryDate) VALUES (1, 1, '2025-07-01 10:00:00', N'Completed', '2025-07-05 10:00:00');
INSERT INTO Orders (OrderID, UserID, OrderDate, Status, DeliveryDate) VALUES (2, 2, '2025-07-02 11:30:00', N'Processing', '2025-07-06 11:30:00');
INSERT INTO Orders (OrderID, UserID, OrderDate, Status, DeliveryDate) VALUES (3, 1, '2025-07-03 14:00:00', N'Pending', '2025-07-07 14:00:00');
INSERT INTO Orders (OrderID, UserID, OrderDate, Status, DeliveryDate) VALUES (4, 3, '2025-07-04 09:15:00', N'Completed', '2025-07-08 09:15:00');
INSERT INTO Orders (OrderID, UserID, OrderDate, Status, DeliveryDate) VALUES (5, 4, '2025-07-05 16:45:00', N'Processing', '2025-07-09 16:45:00');

INSERT INTO OrderItems (OrderItemID, OrderID, ProductID, Quantity, Price) VALUES (1, 1, 1, 1, 149999.00);
INSERT INTO OrderItems (OrderItemID, OrderID, ProductID, Quantity, Price) VALUES (2, 1, 2, 2, 7694.00);
INSERT INTO OrderItems (OrderItemID, OrderID, ProductID, Quantity, Price) VALUES (3, 2, 4, 1, 144999.00);
INSERT INTO OrderItems (OrderItemID, OrderID, ProductID, Quantity, Price) VALUES (4, 3, 5, 1, 69999.00);
INSERT INTO OrderItems (OrderItemID, OrderID, ProductID, Quantity, Price) VALUES (5, 4, 3, 1, 34199.00);
INSERT INTO OrderItems (OrderItemID, OrderID, ProductID, Quantity, Price) VALUES (6, 4, 7, 1, 81999.00);
INSERT INTO OrderItems (OrderItemID, OrderID, ProductID, Quantity, Price) VALUES (7, 5, 6, 1, 299999.00);
INSERT INTO OrderItems (OrderItemID, OrderID, ProductID, Quantity, Price) VALUES (8, 5, 8, 1, 214999.00);

INSERT INTO Warranties (WarrantyID, OrderItemID, StartDate, EndDate) VALUES (1, 1, '2025-07-05 00:00:00', '2026-07-05 00:00:00');
INSERT INTO Warranties (WarrantyID, OrderItemID, StartDate, EndDate) VALUES (2, 3, '2025-07-06 00:00:00', '2027-07-06 00:00:00');
INSERT INTO Warranties (WarrantyID, OrderItemID, StartDate, EndDate) VALUES (3, 5, '2025-07-08 00:00:00', '2026-01-08 00:00:00');

INSERT INTO SpareParts (PartID, ProductID, PartName, Stock, Price) VALUES (1, 1, N'Refrigerator Door Handle', 5, 1500.00);
INSERT INTO SpareParts (PartID, ProductID, PartName, Stock, Price) VALUES (2, 2, N'Mixer Beaters (Set of 2)', 10, 500.00);
INSERT INTO SpareParts (PartID, ProductID, PartName, Stock, Price) VALUES (3, 4, N'TV Remote Control', 8, 1200.00);
INSERT INTO SpareParts (PartID, ProductID, PartName, Stock, Price) VALUES (4, 7, N'Washing Machine Inlet Hose', 15, 750.00);
INSERT INTO SpareParts (PartID, ProductID, PartName, Stock, Price) VALUES (5, 8, N'AC Remote Control', 7, 1000.00);

INSERT INTO Stores (StoreID, Name, Address, Phone, City) VALUES (1, N'Singer Mega - Colombo 04', N'Galle Road, Colombo 04', N'0112580000', N'Colombo');
INSERT INTO Stores (StoreID, Name, Address, Phone, City) VALUES (2, N'Singer Plus - Kandy', N'Peradeniya Road, Kandy', N'0812234567', N'Kandy');
INSERT INTO Stores (StoreID, Name, Address, Phone, City) VALUES (3, N'Singer Showroom - Galle', N'Matara Road, Galle', N'0912223344', N'Galle');
INSERT INTO Stores (StoreID, Name, Address, Phone, City) VALUES (4, N'Singer Showroom - Jaffna', N'Kandy Road, Jaffna', N'0212225566', N'Jaffna');
GO


