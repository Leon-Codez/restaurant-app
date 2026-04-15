from flask import Flask, render_template, request, redirect, session, flash
import psycopg2
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = 'restaurant_secret_key'
bcrypt = Bcrypt(app)

def get_db():
    conn = psycopg2.connect(
        dbname='restaurant',
        user='beyondunderstanding',
        host='localhost',
        port='5432'
    )
    return conn
# Routes for the app
# Home page route
@app.route('/')
def home():
         return render_template('home.html')

# Menu page route
@app.route('/menu')
def menu():
         return render_template('menu.html')

# Cart page route
@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    return render_template('cart.html', cart_items=cart_items)

@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    item = {
        'name': request.form['name'],
        'price': float(request.form['price']),
        'quantity': 1
    }
    # Create cart if it doesn't exist
    if 'cart' not in session:
        session['cart'] = []
    # Check if item already exists → increase quantity
    for cart_item in session['cart']:
        if cart_item['name'] == item['name']:
            cart_item['quantity'] += 1
            break
    else:
        session['cart'].append(item)

    session.modified = True
    flash(f"{item['name']} added to cart!")
    return redirect('/menu')

@app.route('/remove-from-cart', methods=['POST'])
def remove_from_cart():
    name = request.form['name']

    if 'cart' in session:
        session['cart'] = [item for item in session['cart'] if item['name'] != name]
        session.modified = True

    flash(f"{name} removed from cart")
    return redirect('/cart')

# Order confirmation route
@app.route('/order-confirmation')
def order_confirmation():
    return render_template('order_confirmation.html')

# Staff login route
@app.route('/staff-login')
def staff_login():
    return render_template('staff_login.html')

# Kitchen access route
@app.route('/kitchen')
def kitchen():
    if 'staff_id' not in session:
        return redirect('/staff-login')
    return render_template('kitchen.html')

# Manager access route
@app.route('/manager')
def manager():
    if 'staff_id' not in session:
        return redirect('/staff-login')
    if session['role'] != 'manager':
        return redirect('/kitchen')
    return render_template('manager.html')

if __name__ == '__main__':
    app.run(debug=True)
