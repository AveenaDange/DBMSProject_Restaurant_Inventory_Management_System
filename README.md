

---

# **Samosa and Company Database Project**

Welcome to the **Samosa and Company Database Project**! This project involves designing and implementing a relational database for a fictional company that specializes in managing inventory, supplier relationships, employee tasks, and orders for a streamlined and efficient business operation.

---

## **Table of Contents**

1. [About the Project](#about-the-project)
2. [Database Schema](#database-schema)
3. [Features](#features)
4. [Setup and Installation](#setup-and-installation)
5. [Usage](#usage)
6. [Contributing](#contributing)
7. [License](#license)

---

## **About the Project**

**SamosaDB** is a database designed to support the operational needs of Samosa and Company. The system manages user roles, product inventory, supplier information, and employee tasks while ensuring data consistency and reliability through robust relational design principles.

The database is optimized for:

- **Efficient Inventory Management**  
- **Tracking Supplier Orders**  
- **Task Assignment and Monitoring for Employees**  

This project demonstrates key database management concepts such as **normalization**, **indexing**, and **transaction management**.

---

## **Database Schema**

The database consists of the following tables:

### 1. **Users**
Manages user information, such as owners, employees, and suppliers.
- **Columns:** `UserID`, `Name`, `Email`, `RoleID`

### 2. **Roles**
Stores user roles for normalization.
- **Columns:** `RoleID`, `RoleName`

### 3. **Products**
Tracks inventory details.
- **Columns:** `ProductID`, `Name`, `Description`, `Quantity`, `Price`, `ReorderLevel`

### 4. **Suppliers**
Stores supplier details.
- **Columns:** `SupplierID`, `Name`, `Contact`, `Address`

### 5. **Orders**
Manages supplier orders.
- **Columns:** `OrderID`, `SupplierID`, `OrderDate`, `TotalAmount`

### 6. **OrderDetails**
Links orders to specific products.
- **Columns:** `OrderDetailID`, `OrderID`, `ProductID`, `Quantity`, `UnitPrice`

### 7. **Tasks**
Manages employee tasks.
- **Columns:** `TaskID`, `EmployeeID`, `Description`, `Status`, `DueDate`

---

## **Features**

- **CRUD Operations**: Create, Read, Update, Delete functionality for all tables.
- **Role-Based User Management**: Owners, employees, and suppliers managed through the `Roles` table.
- **Inventory Tracking**: Automatic notifications when stock reaches the reorder level.
- **Order Management**: Supplier order processing with detailed breakdowns.
- **Task Assignment**: Allocate and monitor tasks for employees with due dates.

---

## **Setup and Installation**

To set up the SamosaDB project on your local machine:

1. **Clone the Repository**:  
   ```bash
   git clone https://github.com/username/SamosaDB.git
   cd SamosaDB
   ```

2. **Install Dependencies**:  
   Ensure you have a DBMS like MySQL or PostgreSQL installed.

3. **Import the Schema**:  
   Execute the provided SQL script to create the database structure.  
   ```bash
   mysql -u username -p < schema.sql
   ```

4. **Connect to the Database**:  
   Configure your database connection settings in the application (if applicable).

---

## **Usage**

Once the database is set up:

1. Populate the tables with test data using the included seed scripts.  
2. Perform SQL queries to manage inventory, process orders, and assign tasks.  
3. Extend the database with additional features as needed.

---

## **Contributing**

Contributions are welcome! To contribute:

1. Fork the repository.  
2. Create a feature branch:  
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:  
   ```bash
   git commit -m "Added new feature"
   ```
4. Push to the branch:  
   ```bash
   git push origin feature-name
   ```
5. Submit a pull request.

---

## **License**

This project is licensed under the MIT License. See the `LICENSE` file for details.

---
