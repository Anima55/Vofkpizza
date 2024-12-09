from flask import Flask, render_template, session, request, redirect, url_for, g
from models import get_db_connection
from models import init_db
from routes.feedback import feedback_bp
from routes.admin import admin_bp
from routes.shop import shop_bp
from routes.api import api_bp
from routes.user import user_bp
import bcrypt

app = Flask(__name__)
app.secret_key = 'super_secret_key'  

init_db()



app.register_blueprint(feedback_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(shop_bp)
app.register_blueprint(api_bp)
app.register_blueprint(user_bp)



@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/shop')
def shop():
    menu_data = {
        "Піца": [
            {"name": "Маргарита", "price": "120 грн", "ingredients": "Томатний соус, сир моцарелла, базилік", "image": "static/img/pizza_1.png"},
            {"name": "Пеппероні", "price": "150 грн", "ingredients": "Томатний соус, сир моцарелла, пеппероні", "image": "static/img/pizza_2.png"},
            {"name": "Чотири Сира", "price": "170 грн", "ingredients": "Томатний соус, сир моцарелла, пармезан, горгонзола, фета", "image": "static/img/pizza_3.png"},
            {"name": "Гавайська", "price": "200 грн", "ingredients": "Томатний соус, сир моцарелла, ананас, шинка", "image": "static/img/pizza_4.png"},
            {"name": "Карбонара", "price": "140 грн", "ingredients": "Томатний соус, сир моцарелла, ананас", "image": "static/img/pizza_5.png"},
            {"name": "Сицилійська", "price": "140 грн", "ingredients": "Анчоуси, свіжі томати та сир пекорино", "image": "static/img/pizza_6.png"}
        ],
        "Напої безалкогольні": [
            {"name": "Живчик", "price": "30 грн", "ingredients": "Газована вода, цукор, ароматизатори", "image": "static/img/drink_1.png"},
            {"name": "Monster energy", "price": "60 грн", "ingredients": "Газована вода, кофеїн, цукор, ароматизатори", "image": "static/img/drink_2.png"},
            {"name": "Red Bull", "price": "40 грн", "ingredients": "Газована вода, цукор, ароматизатори", "image": "static/img/drink_3.png"},
            {"name": "Reign", "price": "55 грн", "ingredients": "Газована вода, цукор, ароматизатори", "image": "static/img/drink_4.png"},
            {"name": "Coca Cola", "price": "45 грн", "ingredients": "Газована вода, цукор, ароматизатори", "image": "static/img/drink_5.png"},
            {"name": "Fanta", "price": "45 грн", "ingredients": "Газована вода, цукор, ароматизатори", "image": "static/img/drink_6.png"}
        ],
        "Алкогольні напої": [
            {"name": "Пиво", "price": "50 грн", "ingredients": "Солод, вода, хміль, дріжджі", "image": "static/img/alcodrink_1.jpg"}
        ],
        "Новинки": [
            {"name": "Піца від бабусі Галі", "price": "200 грн", "ingredients": "Помідор, шинка, огірок, капуста, томатний соус", "image": "static/img/pizza_7.png"}
        ]
    }

    return render_template('shop.html', menu=menu_data)

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/discount')
def discount():
    return render_template('discount.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    item_name = request.form.get('item_name') 
    item_price = int(request.form.get('item_price').split()[0])  
    item_image = request.form.get('item_image')  

    
    if 'cart' not in session:
        session['cart'] = {}

    cart = session['cart']

    
    if item_name in cart:
        cart[item_name]['quantity'] += 1
    else:
        
        cart[item_name] = {
            'name': item_name,
            'price': item_price,
            'quantity': 1,
            'image': item_image
        }

    session['cart'] = cart  
    session.modified = True  

    return redirect(url_for('shop'))

@app.route('/cart', methods=['GET'])
def cart():
    cart = session.get('cart', {})  
    total = sum(item['price'] * item['quantity'] for item in cart.values()) 
    return render_template('cart.html', cart=cart, total=total)

@app.route('/checkout', methods=['POST'])
def checkout():
    email = request.form.get('email')  
    address = request.form.get('address')  
    cart = session.get('cart', {})  

    if not cart:
        return redirect(url_for('cart'))  

   

    
    session.pop('cart', None)

    return render_template('order_success.html', email=email, address=address)

@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    session.pop('cart', None)  
    return redirect(url_for('cart'))

@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        conn = get_db_connection()
        g.user = conn.execute(
            'SELECT * FROM users WHERE id = ?', (user_id,)
        ).fetchone()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)