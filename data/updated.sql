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
-------------------
CREATE TABLE Users (
    UserID NVARCHAR(10) PRIMARY KEY,  -- e.g., 'USR001'
    Name NVARCHAR(100),
    Email NVARCHAR(100),
    Phone NVARCHAR(20),
    Address NVARCHAR(255)
);

CREATE TABLE Categories (
    CategoryID NVARCHAR(10) PRIMARY KEY,  -- e.g., 'CAT001'
    Name NVARCHAR(100),
    Description NVARCHAR(255)
);

CREATE TABLE Products (
    ProductID NVARCHAR(10) PRIMARY KEY,  -- e.g., 'PRD001'
    Name NVARCHAR(100),
    CategoryID NVARCHAR(10) FOREIGN KEY REFERENCES Categories(CategoryID),
    Description NVARCHAR(255),
    Price DECIMAL(10, 2),
    Stock INT
);

CREATE TABLE Orders (
    OrderID NVARCHAR(10) PRIMARY KEY,  -- e.g., 'ORD001'
    UserID NVARCHAR(10) FOREIGN KEY REFERENCES Users(UserID),
    OrderDate DATETIME,
    Status NVARCHAR(50),
    DeliveryDate DATETIME
);

CREATE TABLE OrderItems (
    OrderItemID NVARCHAR(10) PRIMARY KEY,  -- e.g., 'OIT001'
    OrderID NVARCHAR(10) FOREIGN KEY REFERENCES Orders(OrderID),
    ProductID NVARCHAR(10) FOREIGN KEY REFERENCES Products(ProductID),
    Quantity INT,
    Price DECIMAL(10, 2)
);

CREATE TABLE Warranties (
    WarrantyID NVARCHAR(10) PRIMARY KEY,  -- e.g., 'WAR001'
    OrderItemID NVARCHAR(10) FOREIGN KEY REFERENCES OrderItems(OrderItemID),
    StartDate DATETIME,
    EndDate DATETIME
);

CREATE TABLE SpareParts (
    PartID NVARCHAR(10) PRIMARY KEY,  -- e.g., 'SPT001'
    ProductID NVARCHAR(10) FOREIGN KEY REFERENCES Products(ProductID),
    PartName NVARCHAR(100),
    Stock INT,
    Price DECIMAL(10, 2)
);

CREATE TABLE Stores (
    StoreID NVARCHAR(10) PRIMARY KEY,  -- e.g., 'STR001'
    Name NVARCHAR(100),
    Address NVARCHAR(255),
    Phone NVARCHAR(20),
    City NVARCHAR(50)
);
-- Users
INSERT INTO Users (UserID, Name, Email, Phone, Address) VALUES
('USR001', N'Alice Smith', N'alice.smith@example.com', N'0771234567', N'123 Main St, Colombo'),
('USR002', N'Bob Johnson', N'bob.j@example.com', N'0719876543', N'456 High St, Kandy'),
('USR003', N'Catherine Lee', N'cathy.l@example.com', N'0765432109', N'789 Oak Ave, Galle'),
('USR004', N'David Chen', N'david.c@example.com', N'0701122334', N'101 Pine Rd, Jaffna'),
('USR005', N'Eva Green', N'eva.g@example.com', N'0758899001', N'202 Elm St, Negombo');

-- Categories
INSERT INTO Categories (CategoryID, Name, Description) VALUES
('CAT001', N'Electronics', N'Electronics and IT related products'),
('CAT002', N'Home Appliances', N'Appliances for home use'),
('CAT003', N'Kitchen Appliances', N'Appliances for kitchen use'),
('CAT004', N'TV & Audio', N'Entertainment and smart home devices'),
('CAT005', N'Furniture', N'Home and office furniture');

-- Products
INSERT INTO Products (ProductID, Name, CategoryID, Description, Price, Stock) VALUES
('PRD001', N'Sisil Inverter Refrigerator SL-INV-285H', 'CAT002', N'No Frost, 285L', 149999.00, 10),
('PRD002', N'Singer Hand Mixer KA-HM-01', 'CAT003', N'360W, 5 Speeds', 7694.00, 50),
('PRD003', N'Singer Kitchen Machine 5L, 1400W', 'CAT003', N'5L, 1400W', 34199.00, 20),
('PRD004', N'Panasonic 43" 4K Smart Google TV', 'CAT004', N'TH-43PX740N', 144999.00, 15),
('PRD005', N'Honor 200 Smart 5G', 'CAT001', N'8GB / 256GB, White', 69999.00, 30);

-- Orders
INSERT INTO Orders (OrderID, UserID, OrderDate, Status, DeliveryDate) VALUES
('ORD001', 'USR001', '2025-07-01 10:00:00', N'Completed', '2025-07-05 10:00:00'),
('ORD002', 'USR002', '2025-07-02 11:30:00', N'Processing', '2025-07-06 11:30:00'),
('ORD003', 'USR003', '2025-07-03 14:00:00', N'Pending', '2025-07-07 14:00:00'),
('ORD004', 'USR004', '2025-07-04 09:15:00', N'Completed', '2025-07-08 09:15:00'),
('ORD005', 'USR005', '2025-07-05 16:45:00', N'Processing', '2025-07-09 16:45:00');

-- OrderItems
INSERT INTO OrderItems (OrderItemID, OrderID, ProductID, Quantity, Price) VALUES
('OIT001', 'ORD001', 'PRD001', 1, 149999.00),
('OIT002', 'ORD001', 'PRD002', 2, 7694.00),
('OIT003', 'ORD002', 'PRD004', 1, 144999.00),
('OIT004', 'ORD003', 'PRD005', 1, 69999.00),
('OIT005', 'ORD004', 'PRD003', 1, 34199.00);

-- Warranties
INSERT INTO Warranties (WarrantyID, OrderItemID, StartDate, EndDate) VALUES
('WAR001', 'OIT001', '2025-07-05 00:00:00', '2026-07-05 00:00:00'),
('WAR002', 'OIT002', '2025-07-05 00:00:00', '2026-07-05 00:00:00'),
('WAR003', 'OIT003', '2025-07-06 00:00:00', '2027-07-06 00:00:00'),
('WAR004', 'OIT004', '2025-07-07 00:00:00', '2026-07-07 00:00:00'),
('WAR005', 'OIT005', '2025-07-08 00:00:00', '2026-01-08 00:00:00');

-- SpareParts
INSERT INTO SpareParts (PartID, ProductID, PartName, Stock, Price) VALUES
('SPT001', 'PRD001', N'Refrigerator Door Handle', 5, 1500.00),
('SPT002', 'PRD002', N'Mixer Beaters (Set of 2)', 10, 500.00),
('SPT003', 'PRD004', N'TV Remote Control', 8, 1200.00),
('SPT004', 'PRD003', N'Kitchen Machine Bowl', 6, 2500.00),
('SPT005', 'PRD005', N'Smartphone Charger', 15, 2000.00);

-- Stores
INSERT INTO Stores (StoreID, Name, Address, Phone, City) VALUES
('STR001', N'Singer Mega - Colombo 04', N'Galle Road, Colombo 04', N'0112580000', N'Colombo'),
('STR002', N'Singer Plus - Kandy', N'Peradeniya Road, Kandy', N'0812234567', N'Kandy'),
('STR003', N'Singer Showroom - Galle', N'Matara Road, Galle', N'0912223344', N'Galle'),
('STR004', N'Singer Showroom - Jaffna', N'Kandy Road, Jaffna', N'0212225566', N'Jaffna'),
('STR005', N'Singer Plus - Negombo', N'Negombo Road, Negombo', N'0312233445', N'Negombo');