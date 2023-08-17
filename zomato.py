import json
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_socketio import SocketIO, emit,socketio


app = Flask(__name__)
@socketio.on('connect', namespace='/status')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect', namespace='/status')
def handle_disconnect():
    print('Client disconnected')

app.secret_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiw'
# Save data to a file


def save_data(menu, orders):
    data = {
        "menu": menu,
        "orders": orders
    }
    with open("data.json", "w") as file:
        json.dump(data, file)

# Load data from a file


def load_data():
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
            menu = data.get("menu", [])
            orders = data.get("orders", [])
            return menu, orders
    except FileNotFoundError:
        return [], []

# Main program


@app.route('/')
def index():
    return 'Welcome to Zesty Zomato!'


@app.route('/menu')
def display_menu():
    return render_template('menu.html', menu=menu)

# zomato.py

# ... existing code ...


@app.route('/add_dish', methods=['GET', 'POST'])
def add_dish():
    if request.method == 'POST':
        dish_name = request.form['dish_name']
        price = float(request.form['price'])

        # Create a new dish
        dish_id = len(menu) + 1
        dish = {
            'id': dish_id,
            'name': dish_name,
            'price': price,
            'availability': True,
        }

        # Add the new dish to the menu
        menu.append(dish)

        # Save the updated menu to the file
        save_data(menu, orders)

        return redirect(url_for('display_menu'))

    return render_template('add_dish.html')


# zomato.py

# ... existing code ...
@app.route('/remove_dish/<int:dish_id>', methods=['GET', 'POST'])
def remove_dish(dish_id):
    dish_id = int(dish_id)
    dish = find_dish_by_id(menu, dish_id)

    if dish is None:
        flash('Dish not found.')
        return redirect(url_for('display_menu'))

    if request.method == 'POST':
        menu.remove(dish)
        save_data(menu, orders)

        flash('Dish removed successfully.')
        return redirect(url_for('display_menu'))

    return render_template('remove_dish.html', dish=dish)


# zomato.py

# ... existing code ...
@app.route('/update_availability/<int:dish_id>', methods=['GET', 'POST'])
def update_availability(dish_id):
    dish = find_dish_by_id(menu, dish_id)

    if dish is None:
        return render_template('dish_not_found.html')

    if request.method == 'POST':
        availability = request.form.get('availability')
        dish['availability'] = (availability == 'available')
        save_data(menu, orders)

        flash('Availability updated successfully.')
        return redirect(url_for('display_menu'))

    return render_template('update_availability.html', dish=dish)


@app.route('/take_order', methods=['GET', 'POST'])
def take_order():
    if request.method == 'POST':
        customer_name = request.form.get('customer_name')
        dish_ids = request.form.getlist('dish_ids')

        # Validate if customer name and dish IDs are provided
        if not customer_name or not dish_ids:
            flash('Please provide customer name and select at least one dish.')
            return redirect(url_for('display_menu'))

        # Convert dish IDs to integers
        dish_ids = [int(dish_id) for dish_id in dish_ids]

        # Create the order
        order_id = len(orders) + 1
        order = {
            'id': order_id,
            'customer_name': customer_name,
            'dishes': [],
            'status': 'received'
        }

        # Add selected dishes to the order
        for dish_id in dish_ids:
            dish = find_dish_by_id(menu, dish_id)
            if dish:
                order['dishes'].append(dish)

        # Add the order to the orders list
        orders.append(order)
        save_data(menu, orders)

        flash('Order placed successfully.')
        return redirect(url_for('display_menu'))

    return render_template('take_order.html', menu=menu)

@app.route('/review_orders')
def review_orders():
    status_filter = request.args.get('status')
    filtered_orders = [order for order in orders if order['status'] == status_filter] if status_filter else orders
    for order in filtered_orders:
        total_price = 0
        for dish in order['dishes']:
            total_price += dish['price']
        order['total_price'] = total_price
    return render_template('review_orders.html', orders=filtered_orders)


@app.route('/update_order_status/<int:order_id>', methods=['GET', 'POST'])
def update_order_status(order_id):
    order = find_order_by_id(orders, order_id)

    if order is None:
        return render_template('order_not_found.html')

    if request.method == 'POST':
        status = request.form['status']
        order['status'] = status
        save_data(menu, orders)

        flash('Order status updated successfully.')
        return redirect(url_for('review_orders'))

    return render_template('update_order_status.html', order=order)


# Load data from the file


def find_dish_by_id(menu, dish_id):
    for dish in menu:
        if dish["id"] == dish_id:
            return dish
    return None


def find_order_by_id(orders, order_id):
    for order in orders:
        if order['id'] == order_id:
            return order
    return None


if __name__ == '__main__':
    app.secret_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiw'
    menu, orders = load_data()
    for order in orders:
    socketio.emit('order_status_update', {'order_id': order['id'], 'status': order['status']}, namespace='/status')

    app.run()
