from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
import time
import threading
from datetime import datetime

app = Flask(__name__)
CORS(app)

def get_db_connection():
    """Create a new database connection"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="enter your password",
            database="vyra_food_tracker",
            connection_timeout=30,
            autocommit=False
        )
        print("✅ Database connected successfully")
        return connection
    except Error as e:
        print(f"❌ Database connection error: {e}")
        return None

def get_cursor():
    """Get database cursor with fresh connection if needed"""
    global db
    try:
        if db is None or not db.is_connected():
            db = get_db_connection()
        return db, db.cursor(dictionary=True)
    except Exception as e:
        print(f"Cursor error: {e}")
        db = get_db_connection()
        if db:
            return db, db.cursor(dictionary=True)
        return None, None


db = get_db_connection()

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/menu')
def menu_page():
    return render_template('menu.html')

@app.route('/place_order_page')
def place_order_page():
    return render_template('order.html')

@app.route('/track')
def track_page():
    return render_template('track.html')

@app.route('/cart_page')
def cart_page():
    return render_template('cart.html')


@app.route('/api/menu', methods=['GET'])
def get_menu():
    try:
        conn, cursor = get_cursor()
        if conn is None or cursor is None:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor.execute("""
            SELECT 
                m.item_id,
                m.item_name,
                m.price,
                r.name AS restaurant
            FROM menu m
            JOIN restaurants r 
            ON m.restaurant_id = r.restaurant_id
            LIMIT 50
        """)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        print(f"Error in get_menu: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/users', methods=['GET'])
def get_users():
    try:
        conn, cursor = get_cursor()
        if conn is None or cursor is None:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor.execute("SELECT * FROM users LIMIT 5")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    if not data or not data.get('name') or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Missing required fields"}), 400
    try:
        conn, cursor = get_cursor()
        if conn is None or cursor is None:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (data['name'], data['email'], data['password'])
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "User added successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/update_user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    try:
        conn, cursor = get_cursor()
        if conn is None or cursor is None:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor.execute(
            "UPDATE users SET name=%s, email=%s, password=%s WHERE user_id=%s",
            (data.get('name'), data.get('email'), data.get('password'), user_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": f"User {user_id} updated successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        conn, cursor = get_cursor()
        if conn is None or cursor is None:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor.execute("DELETE FROM users WHERE user_id=%s", (user_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": f"User {user_id} deleted successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    if not data or not data.get('user_id') or not data.get('item_id'):
        return jsonify({"error": "user_id and item_id required"}), 400
    
    try:
        conn, cursor = get_cursor()
        if conn is None or cursor is None:
            return jsonify({"error": "Database connection failed"}), 500
        
        user_id = data['user_id']
        item_id = data['item_id']
        quantity = data.get('quantity', 1)
        
        cursor.execute(
            "SELECT cart_id, quantity FROM cart WHERE user_id = %s AND item_id = %s",
            (user_id, item_id)
        )
        existing = cursor.fetchone()
        
        if existing:
            new_quantity = existing['quantity'] + quantity
            cursor.execute(
                "UPDATE cart SET quantity = %s WHERE cart_id = %s",
                (new_quantity, existing['cart_id'])
            )
        else:
            cursor.execute(
                "INSERT INTO cart (user_id, item_id, quantity) VALUES (%s, %s, %s)",
                (user_id, item_id, quantity)
            )
        
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Item added to cart successfully!"})
        
    except Exception as e:
        print(f"Error in add_to_cart: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/cart/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    try:
        conn, cursor = get_cursor()
        if conn is None or cursor is None:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor.execute("""
            SELECT 
                c.cart_id,
                c.user_id,
                c.item_id,
                c.quantity,
                m.item_name,
                m.price,
                r.name AS restaurant
            FROM cart c
            JOIN menu m ON c.item_id = m.item_id
            JOIN restaurants r ON m.restaurant_id = r.restaurant_id
            WHERE c.user_id = %s
        """, (user_id,))
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/cart/update', methods=['PUT'])
def update_cart_item():
    data = request.get_json()
    if not data or not data.get('cart_id') or data.get('quantity') is None:
        return jsonify({"error": "cart_id and quantity required"}), 400
    
    try:
        conn, cursor = get_cursor()
        if conn is None or cursor is None:
            return jsonify({"error": "Database connection failed"}), 500
        
        quantity = data['quantity']
        
        if quantity <= 0:
            cursor.execute("DELETE FROM cart WHERE cart_id = %s", (data['cart_id'],))
        else:
            cursor.execute(
                "UPDATE cart SET quantity = %s WHERE cart_id = %s",
                (quantity, data['cart_id'])
            )
        
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Cart updated successfully!"})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/cart/remove/<int:cart_id>', methods=['DELETE'])
def remove_from_cart(cart_id):
    try:
        conn, cursor = get_cursor()
        if conn is None or cursor is None:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor.execute("DELETE FROM cart WHERE cart_id = %s", (cart_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Item removed from cart!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/cart/checkout', methods=['POST'])
def checkout_cart():
    data = request.get_json()
    if not data or not data.get('user_id'):
        return jsonify({"error": "user_id required"}), 400
    
    try:
        conn, cursor = get_cursor()
        if conn is None or cursor is None:
            return jsonify({"error": "Database connection failed"}), 500
        
        user_id = data['user_id']
        
        cursor.execute("""
            SELECT c.item_id, c.quantity, m.price
            FROM cart c
            JOIN menu m ON c.item_id = m.item_id
            WHERE c.user_id = %s
        """, (user_id,))
        cart_items = cursor.fetchall()
        
        if not cart_items:
            cursor.close()
            conn.close()
            return jsonify({"error": "Cart is empty"}), 400
        
        total_amount = sum(float(item['price']) * int(item['quantity']) for item in cart_items)
        
        cursor.execute(
            "INSERT INTO orders (user_id, order_time, total_amount) VALUES (%s, NOW(), %s)",
            (user_id, total_amount)
        )
        order_id = cursor.lastrowid
        
        for item in cart_items:
            cursor.execute(
                "INSERT INTO order_items (order_id, item_id, quantity) VALUES (%s, %s, %s)",
                (order_id, item['item_id'], item['quantity'])
            )
        
        cursor.execute(
            "INSERT INTO order_status (order_id, status, updated_time) VALUES (%s, %s, NOW())",
            (order_id, "Order Placed")
        )
        
        cursor.execute("DELETE FROM cart WHERE user_id = %s", (user_id,))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            "message": "Order placed successfully from cart!",
            "order_id": order_id,
            "total_amount": total_amount
        })
        
    except Exception as e:
        print(f"Checkout error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/cart/count/<int:user_id>', methods=['GET'])
def get_cart_count(user_id):
    try:
        conn, cursor = get_cursor()
        if conn is None or cursor is None:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor.execute(
            "SELECT COALESCE(SUM(quantity), 0) as total FROM cart WHERE user_id = %s",
            (user_id,)
        )
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        count = result['total'] if result else 0
        return jsonify({"count": count})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/place_order', methods=['POST'])
def place_order():
    data = request.get_json()
    if not data or not data.get('user_id') or not data.get('items'):
        return jsonify({"error": "user_id and items required"}), 400
    
    try:
        conn, cursor = get_cursor()
        if conn is None or cursor is None:
            return jsonify({"error": "Database connection failed"}), 500
        
        total_amount = 0
        for item in data['items']:
            cursor.execute("SELECT price FROM menu WHERE item_id = %s", (item['item_id'],))
            result = cursor.fetchone()
            if result:
                total_amount += float(result['price']) * int(item['quantity'])
        
        cursor.execute(
            "INSERT INTO orders (user_id, order_time, total_amount) VALUES (%s, NOW(), %s)",
            (data['user_id'], total_amount)
        )
        order_id = cursor.lastrowid
        
        for item in data['items']:
            if int(item['quantity']) > 0:
                cursor.execute(
                    "INSERT INTO order_items (order_id, item_id, quantity) VALUES (%s, %s, %s)",
                    (order_id, item['item_id'], item['quantity'])
                )
        
        cursor.execute(
            "INSERT INTO order_status (order_id, status, updated_time) VALUES (%s, %s, NOW())",
            (order_id, "Order Placed")
        )
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            "message": "Order placed successfully!",
            "order_id": order_id,
            "total_amount": total_amount
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/order_status/<int:order_id>', methods=['GET'])
def get_order_status(order_id):
    try:
        conn, cursor = get_cursor()
        if conn is None or cursor is None:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor.execute("""
            SELECT status, updated_time
            FROM order_status
            WHERE order_id = %s
            ORDER BY updated_time DESC
            LIMIT 1
        """, (order_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if result:
            return jsonify(result)
        else:
            return jsonify({"status": "Order Placed", "updated_time": None})
    except Exception as e:
        print(f"Error in order_status: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/order_history/<int:order_id>', methods=['GET'])
def order_history(order_id):
    try:
        conn, cursor = get_cursor()
        if conn is None or cursor is None:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor.execute("""
            SELECT status, updated_time
            FROM order_status
            WHERE order_id = %s
            ORDER BY updated_time ASC
        """, (order_id,))
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        
        if result:
            return jsonify(result)
        else:
            return jsonify([])
    except Exception as e:
        print(f"Error in order_history: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/user_orders/<int:user_id>', methods=['GET'])
def user_orders(user_id):
    try:
        conn, cursor = get_cursor()
        if conn is None or cursor is None:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor.execute("""
            SELECT 
                o.order_id,
                o.order_time,
                o.total_amount,
                COALESCE(os.status, 'Order Placed') as status
            FROM orders o
            LEFT JOIN (
                SELECT order_id, status, 
                       ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY updated_time DESC) as rn
                FROM order_status
            ) os ON o.order_id = os.order_id AND os.rn = 1
            WHERE o.user_id = %s
            ORDER BY o.order_time DESC
        """, (user_id,))
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        
        if result:
            return jsonify(result)
        else:
            return jsonify([])
    except Exception as e:
        print(f"Error in user_orders: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/update_order_status', methods=['POST'])
def update_order_status():
    data = request.get_json()
    if not data or not data.get('order_id') or not data.get('status'):
        return jsonify({"error": "order_id and status required"}), 400
    try:
        conn, cursor = get_cursor()
        if conn is None or cursor is None:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor.execute(
            "INSERT INTO order_status (order_id, status, updated_time) VALUES (%s, %s, NOW())",
            (data['order_id'], data['status'])
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Order status updated successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500




def auto_update_order_status():
    """Automatically updates order status with your timing requirements:
       - Order Placed → Preparing: 5 seconds
       - Preparing → Out for Delivery: 20 seconds total (15 more seconds)
       - Out for Delivery → Delivered: 50 seconds total (30 more seconds)
    """
    while True:
        try:
            conn, cursor = get_cursor()
            if conn is None or cursor is None:
                time.sleep(5)
                continue
            
            cursor.execute("""
                SELECT o.order_id, o.order_time, os.status
                FROM orders o
                JOIN order_status os ON o.order_id = os.order_id
                WHERE os.status_id IN (
                    SELECT MAX(status_id) 
                    FROM order_status 
                    GROUP BY order_id
                )
                AND os.status != 'Delivered'
                AND o.order_time > DATE_SUB(NOW(), INTERVAL 1 HOUR)
            """)
            orders = cursor.fetchall()
            
            for order in orders:
                order_id = order['order_id']
                current_status = order['status']
                order_time = order['order_time']
                
                
                time_diff = (datetime.now() - order_time).total_seconds()
                

                if current_status == 'Order Placed' and time_diff >= 5:
                    cursor.execute(
                        "INSERT INTO order_status (order_id, status, updated_time) VALUES (%s, %s, NOW())",
                        (order_id, 'Preparing')
                    )
                    conn.commit()
                    print(f"✅ Order #{order_id}: Order Placed → Preparing (after {int(time_diff)} sec)")
                
                
                elif current_status == 'Preparing' and time_diff >= 20:
                    cursor.execute(
                        "INSERT INTO order_status (order_id, status, updated_time) VALUES (%s, %s, NOW())",
                        (order_id, 'Out for Delivery')
                    )
                    conn.commit()
                    print(f"✅ Order #{order_id}: Preparing → Out for Delivery (after {int(time_diff)} sec)")
                
                
                elif current_status == 'Out for Delivery' and time_diff >= 50:
                    cursor.execute(
                        "INSERT INTO order_status (order_id, status, updated_time) VALUES (%s, %s, NOW())",
                        (order_id, 'Delivered')
                    )
                    conn.commit()
                    print(f"✅ Order #{order_id}: Out for Delivery → Delivered (after {int(time_diff)} sec)")
            
            cursor.close()
            conn.close()
            
        except Exception as e:
            print(f"⚠️ Auto-updater error: {e}")
        
        
        time.sleep(2)

def start_auto_updater():
    thread = threading.Thread(target=auto_update_order_status, daemon=True)
    thread.start()
    print("=" * 60)
    print("🤖 AUTO ORDER STATUS UPDATER STARTED!")
    print("   📝 Order Placed → 🍳 Preparing: 5 seconds")
    print("   🍳 Preparing → 🚚 Out for Delivery: 20 seconds (15 more seconds)")
    print("   🚚 Out for Delivery → ✅ Delivered: 50 seconds (30 more seconds)")
    print("=" * 60)


start_auto_updater()

if __name__ == '__main__':
    app.run(debug=True)
