from flask import Flask, request, render_template, redirect, url_for,session, flash
import mysql.connector

app = Flask(__name__)

app.secret_key = 'bad233021f5769cdccf375b84616a46b41872bdb55fc7c23e8b1d34b224d5ab0'


# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="SamosaDB"
)
cursor = db.cursor()
@app.route('/')
def home():
    if 'ID' in session:  # Check if the user is logged in
        # Get the user's role from the session
        user_role = session.get('UserType')

        # Redirect based on the user's role
        if user_role == 'Owner':
            return redirect(url_for('owner_dashboard'))  # Redirect to Owner's dashboard
        elif user_role == 'Employee':
            return redirect(url_for('employee_dashboard'))  # Redirect to Employee's dashboard
        elif user_role == 'Supplier':
            return redirect(url_for('supplier_dashboard'))  # Redirect to Supplier's dashboard
        else:
            return render_template('index.html', username=session.get('username'))  # Default homepage for other roles

    else:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))  # Redirect to login page if the user is not logged in

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        session.clear()
        # Extract form data
        username = request.form['username']
        password = request.form['password']
        
        cursor = db.cursor(dictionary=True)
        # Query the database to verify user credentials
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        user = cursor.fetchone()

        if user:
            # Set session variables after successful login
            session['ID'] = user['UserID']
            session['UserType'] = user['Role']
            session['username'] = user['Username']
            flash('Login successful!', 'success')
            
            # Redirect to the home page after successful login
            return redirect(url_for('home'))  

        else:
            flash('Invalid credentials, please try again.', 'danger')
            return redirect(url_for('login'))  # Redirect back to the login page

    return render_template('login.html', title='Login')

@app.before_request
def before_request():
    session.permanent = True  # Keep the session active between requests (optional)
    if 'ID' not in session:
        session.clear()  # Clear the session before each request to force login every time

@app.route('/owner_dashboard')
def owner_dashboard():
    if 'ID' not in session or session.get('UserType') != 'Owner':
        flash("Please log in as an Owner.", "warning")
        return redirect(url_for('login'))  # Redirect to login if not logged in as Owner
    return render_template('owner_dashboard.html')  # Owner-specific dashboard

@app.route('/employee_dashboard')
def employee_dashboard():
    if 'ID' not in session or session.get('UserType') != 'Employee':
        flash("Please log in as an Employee.", "warning")
        return redirect(url_for('login'))  # Redirect to login if not logged in as Employee
    return render_template('employee_dashboard.html')  # Employee-specific dashboard

@app.route('/supplier_dashboard')
def supplier_dashboard():
    if 'ID' not in session or session.get('UserType') != 'Supplier':
        flash("Please log in as a Supplier.", "warning")
        return redirect(url_for('login'))  # Redirect to login if not logged in as Supplier
    return render_template('supplier_dashboard.html')  # Supplier-specific dashboard

# Logout route to clear the session and log out the user
@app.route('/logout')
def logout():
    session.clear()  # Clear the session data
    flash('You have been logged out!', 'info')
    return redirect(url_for('login'))  # Redirect to login page




# User management routes
# Route to view all users
@app.route('/users')
def view_users():
    cursor.execute("SELECT * FROM Users")
    users = cursor.fetchall()
    return render_template('users.html', users=users)

# Route to add a user
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        contact = request.form['contact']

        cursor.execute(
            "INSERT INTO Users (Username, Password, Role, Contact) VALUES (%s, %s, %s, %s)",
            (username, password, role, contact)
        )
        db.commit()
        return redirect(url_for('view_users'))
    return render_template('add_user.html')

# Route to edit a user
@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    try:
        if request.method == 'POST':
            # Retrieve form data
            username = request.form['username']
            password = request.form['password']
            role = request.form['role']
            contact = request.form['contact']

            # Update user details in the database
            cursor.execute(
                "UPDATE Users SET Username=%s, Password=%s, Role=%s, Contact=%s WHERE UserID=%s",
                (username, password, role, contact, user_id)
            )
            db.commit()  # Save changes to the database

            # Redirect to the list of users after update
            return redirect(url_for('view_users'))

        # Fetch current user data for editing
        cursor.execute("SELECT * FROM Users WHERE UserID=%s", (user_id,))
        user = cursor.fetchone()

        return render_template('edit_user.html', user=user)

    except Exception as e:
        print("Error updating user:", e)
        return f"An error occurred while updating the user: {e}"



# Route to delete a user by their ID
@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    cursor.execute("DELETE FROM Users WHERE UserID = %s", (user_id,))
    db.commit()
    return redirect(url_for('view_users'))

# Product management routes
# Route to view all products
@app.route('/products')
def view_products():
    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()
    return render_template('products.html', products=products)

# Route to add a product
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        quantity = request.form['quantity']
        price = request.form['price']
        reorder_level = request.form['reorder_level']

        cursor.execute(
            "INSERT INTO Products (Name, Description, Quantity, Price, ReorderLevel) VALUES (%s, %s, %s, %s, %s)",
            (name, description, quantity, price, reorder_level)
        )
        db.commit()
        return redirect(url_for('view_products'))
    return render_template('add_product.html')

# Route to update a product
@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    if request.method == 'POST':
        # Retrieve form data
        name = request.form['name']
        description = request.form['description']
        quantity = request.form['quantity']
        price = request.form['price']
        reorder_level = request.form['reorder_level']

        # Update product in the database
        cursor.execute(
            "UPDATE Products SET Name=%s, Description=%s, Quantity=%s, Price=%s, ReorderLevel=%s WHERE ProductID=%s",
            (name, description, quantity, price, reorder_level, product_id)
        )
        db.commit()  # Save the changes to the database
        return redirect(url_for('view_products'))  # Redirect to the product list

    # Fetch the current product details to display in the form
    cursor.execute("SELECT * FROM Products WHERE ProductID=%s", (product_id,))
    product = cursor.fetchone()
    
    return render_template('edit_product.html', product=product)  # Render the edit product template


# Route to delete a product by its ID
@app.route('/delete_product/<int:product_id>')
def delete_product(product_id):
    cursor.execute("DELETE FROM Products WHERE ProductID = %s", (product_id,))
    db.commit()
    return redirect(url_for('view_products'))

# Supplier management routes
# Route to view all suppliers
@app.route('/suppliers')
def view_suppliers():
    cursor.execute("SELECT * FROM Suppliers")
    suppliers = cursor.fetchall()
    return render_template('suppliers.html', suppliers=suppliers)

# Route to add a supplier
@app.route('/add_supplier', methods=['GET', 'POST'])
def add_supplier():
    if request.method == 'POST':
        name = request.form['name']
        contact = request.form['contact']
        email = request.form['email']
        address = request.form['address']

        cursor.execute(
            "INSERT INTO Suppliers (Name, Contact, Email, Address) VALUES (%s, %s, %s, %s)",
            (name, contact, email, address)
        )
        db.commit()
        return redirect(url_for('view_suppliers'))
    return render_template('add_supplier.html')

# Route to update a supplier
@app.route('/edit_supplier/<int:supplier_id>', methods=['GET', 'POST'])
def edit_supplier(supplier_id):
    if request.method == 'POST':
        name = request.form['name']
        contact = request.form['contact']
        email = request.form['email']
        address = request.form['address']

        cursor.execute(
            "UPDATE Suppliers SET Name=%s, Contact=%s, Email=%s, Address=%s WHERE SupplierID=%s",
            (name, contact, email, address, supplier_id)
        )
        db.commit()
        return redirect(url_for('view_suppliers'))

    cursor.execute("SELECT * FROM Suppliers WHERE SupplierID=%s", (supplier_id,))
    supplier = cursor.fetchone()
    return render_template('edit_supplier.html', supplier=supplier)

# Route to delete a supplier by their ID
@app.route('/delete_supplier/<int:supplier_id>')
def delete_supplier(supplier_id):
    cursor.execute("DELETE FROM Suppliers WHERE SupplierID = %s", (supplier_id,))
    db.commit()
    return redirect(url_for('view_suppliers'))

# Order management routes
# Route to view all orders
@app.route('/orders')
def view_orders():
    cursor.execute("""
        SELECT 
            o.OrderID, 
            s.Name AS SupplierName, 
            o.OrderDate, 
            o.TotalAmount 
        FROM 
            Orders o
        JOIN 
            Suppliers s ON o.SupplierID = s.SupplierID
    """)
    orders = cursor.fetchall()  # Fetch all orders along with supplier names
    return render_template('orders.html', orders=orders)  # Render the orders template


# Route to display the add order form and create a new order
@app.route('/make_order', methods=['GET', 'POST'])
def add_order():
    if request.method == 'POST':
        supplier_id = request.form['supplier_id']
        order_date = request.form['order_date']
        total_amount = request.form['total_amount']

        # Insert the new order into the Orders table
        cursor.execute(
            "INSERT INTO Orders (SupplierID, OrderDate, TotalAmount) VALUES (%s, %s, %s)",
            (supplier_id, order_date, total_amount)
        )
        db.commit()  # Commit the new order to the database

        return redirect(url_for('view_orders'))  # Redirect to the list of orders

    # If it's a GET request, fetch suppliers and render the form
    cursor.execute("SELECT * FROM Suppliers")
    suppliers = cursor.fetchall()  # Fetch all suppliers
    return render_template('make_order.html', suppliers=suppliers)  # Pass suppliers to the template


@app.route('/edit_order/<int:order_id>', methods=['GET', 'POST'])
def edit_order(order_id):
    if request.method == 'POST':
        supplier_id = request.form['supplier_id']
        order_date = request.form['order_date']
        total_amount = request.form['total_amount']

        cursor.execute(
            "UPDATE Orders SET SupplierID=%s, OrderDate=%s, TotalAmount=%s WHERE OrderID=%s",
            (supplier_id, order_date, total_amount, order_id)
        )
        db.commit()
        return redirect(url_for('view_orders'))

    # Fetch the existing order details
    cursor.execute("SELECT * FROM Orders WHERE OrderID=%s", (order_id,))
    order = cursor.fetchone()

    # Fetch the list of suppliers for the dropdown
    cursor.execute("SELECT SupplierID, Name FROM Suppliers")
    suppliers = cursor.fetchall()

    return render_template('edit_order.html', order=order, suppliers=suppliers)

# Route to delete an order by its ID
@app.route('/delete_order/<int:order_id>')
def delete_order(order_id):
    cursor.execute("DELETE FROM Orders WHERE OrderID = %s", (order_id,))
    db.commit()
    return redirect(url_for('view_orders'))

# Task management routes
@app.route('/tasks')
def view_tasks():
    cursor.execute("""
        SELECT Tasks.TaskID, Users.Username, Tasks.Description, Tasks.Status, Tasks.DueDate 
        FROM Tasks
        JOIN Users ON Tasks.AssignedTo = Users.UserID
    """)
    tasks = cursor.fetchall()
    return render_template('tasks.html', tasks=tasks)

@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    # Fetch users for the dropdown
    cursor.execute("SELECT UserID, Username FROM Users")
    users = cursor.fetchall()

    if request.method == 'POST':
        assigned_to = request.form['assigned_to']
        description = request.form['description']
        status = request.form['status']
        due_date = request.form['due_date']

        cursor.execute(
            "INSERT INTO Tasks (AssignedTo, Description, Status, DueDate) VALUES (%s, %s, %s, %s)",
            (assigned_to, description, status, due_date)
        )
        db.commit()
        return redirect(url_for('view_tasks'))

    return render_template('add_task.html', users=users)

@app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    # Fetch users for the dropdown
    cursor.execute("SELECT UserID, Username FROM Users")
    users = cursor.fetchall()

    if request.method == 'POST':
        assigned_to = request.form['assigned_to']
        description = request.form['description']
        status = request.form['status']
        due_date = request.form['due_date']

        cursor.execute(
            "UPDATE Tasks SET AssignedTo=%s, Description=%s, Status=%s, DueDate=%s WHERE TaskID=%s",
            (assigned_to, description, status, due_date, task_id)
        )
        db.commit()
        return redirect(url_for('view_tasks'))

    # Fetch the task details for the given task_id
    cursor.execute("SELECT * FROM Tasks WHERE TaskID=%s", (task_id,))
    task = cursor.fetchone()
    return render_template('edit_task.html', task=task, users=users)


# Route to delete a task by its ID
@app.route('/delete_task/<int:task_id>')
def delete_task(task_id):
    cursor.execute("DELETE FROM Tasks WHERE TaskID = %s", (task_id,))
    db.commit()
    return redirect(url_for('view_tasks'))

if __name__ == '__main__':
    app.run(debug=True)
