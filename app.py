from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'    # Replace with your MySQL username
app.config['MYSQL_PASSWORD'] = '1721'  # Replace with your MySQL password
app.config['MYSQL_DB'] = 'product_db'

# Function to get a MySQL connection
def get_db_connection():
    connection = pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB'],
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

# Home page to display all products
@app.route('/')
def index():
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Product")
        products = cursor.fetchall()
    connection.close()
    return render_template('index.html', products=products)

# Create a new product
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        cost = request.form['cost']
        price = request.form['price']
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO Product (Name, Cost, Price) VALUES (%s, %s, %s)", (name, cost, price))
            connection.commit()
        connection.close()
        return redirect(url_for('index'))
    return render_template('create.html')

# Edit a product
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    connection = get_db_connection()
    if request.method == 'POST':
        name = request.form['name']
        cost = request.form['cost']
        price = request.form['price']
        with connection.cursor() as cursor:
            cursor.execute("UPDATE Product SET Name=%s, Cost=%s, Price=%s WHERE Id=%s", (name, cost, price, id))
            connection.commit()
        connection.close()
        return redirect(url_for('index'))

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Product WHERE Id=%s", (id,))
        product = cursor.fetchone()
    connection.close()
    return render_template('edit.html', product=product)

# Delete a product
@app.route('/delete/<int:id>')
def delete(id):
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM Product WHERE Id=%s", (id,))
        connection.commit()
    connection.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)