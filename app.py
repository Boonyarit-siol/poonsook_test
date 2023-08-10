from flask import Flask, render_template, request

app = Flask(__name__)

class Product:
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity

class User:
    def __init__(self, username):
        self.username = username

class ShoppingCart:
    def __init__(self):
        self.products = []

    def add_product(self, product, quantity):
        self.products.append((product, quantity))

    def remove_product(self, product):
        self.products = [(p, q) for p, q in self.products if p != product]

    def confirm_purchase(self):
        for product, quantity in self.products:
            product.quantity -= quantity
        self.products = []

# Create products
products = [
    Product("Bottled water", 10),
    Product("Steamed rice", 6),
    Product("Bananas", 12),
    Product("Loaves of bread", 5),
    Product("Bottles of milk", 3)
]

user = User("user123")

cart = ShoppingCart()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        if username == user.username:
            return render_template('home.html', user=user, products=products)
    return render_template('login.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        for product in products:
            quantity_key = f'quantity_{product.name}'
            if quantity_key in request.form:
                quantity_value = request.form[quantity_key]
                if quantity_value and quantity_value.isdigit():
                    quantity = int(quantity_value)
                    if 0 < quantity <= product.quantity:
                        cart.add_product(product, quantity)
                        product.quantity -= quantity
    return render_template('home.html', user=user, products=products)

if __name__ == '__main__':
    app.run(debug=True)
