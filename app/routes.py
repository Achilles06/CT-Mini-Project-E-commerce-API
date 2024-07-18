from flask import request, jsonify, current_app as app
from .models import (
    Customer, CustomerAccount, Product, Order, OrderItem,
    db, CustomerSchema, CustomerAccountSchema, ProductSchema,
    OrderSchema, OrderItemSchema
)
from datetime import datetime

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)
account_schema = CustomerAccountSchema()
accounts_schema = CustomerAccountSchema(many=True)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)
order_item_schema = OrderItemSchema()
order_items_schema = OrderItemSchema(many=True)

@app.route('/customers', methods=['POST'])
def add_customer():
    data = request.get_json()
    new_customer = Customer(name=data['name'], email=data['email'], phone_number=data['phone_number'])
    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer), 201

@app.route('/customers/<int:id>', methods=['GET'])
def get_customer(id):
    customer = Customer.query.get_or_404(id)
    return customer_schema.jsonify(customer)

@app.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    customer = Customer.query.get_or_404(id)
    data = request.get_json()
    customer.name = data['name']
    customer.email = data['email']
    customer.phone_number = data['phone_number']
    db.session.commit()
    return customer_schema.jsonify(customer)

@app.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": "Customer deleted successfully"})

@app.route('/customer_accounts', methods=['POST'])
def add_customer_account():
    data = request.get_json()
    new_account = CustomerAccount(username=data['username'], password=data['password'], customer_id=data['customer_id'])
    db.session.add(new_account)
    db.session.commit()
    return account_schema.jsonify(new_account), 201

@app.route('/customer_accounts/<int:id>', methods=['GET'])
def get_customer_account(id):
    account = CustomerAccount.query.get_or_404(id)
    return account_schema.jsonify(account)

@app.route('/customer_accounts/<int:id>', methods=['PUT'])
def update_customer_account(id):
    account = CustomerAccount.query.get_or_404(id)
    data = request.get_json()
    account.username = data['username']
    account.password = data['password']
    db.session.commit()
    return account_schema.jsonify(account)

@app.route('/customer_accounts/<int:id>', methods=['DELETE'])
def delete_customer_account(id):
    account = CustomerAccount.query.get_or_404(id)
    db.session.delete(account)
    db.session.commit()
    return jsonify({"message": "Customer account deleted successfully"})

@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    new_product = Product(name=data['name'], price=data['price'], stock=data['stock'])
    db.session.add(new_product)
    db.session.commit()
    return product_schema.jsonify(new_product), 201

@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get_or_404(id)
    return product_schema.jsonify(product)

@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.get_json()
    product.name = data['name']
    product.price = data['price']
    product.stock = data['stock']
    db.session.commit()
    return product_schema.jsonify(product)

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully"})

@app.route('/products', methods=['GET'])
def list_products():
    products = Product.query.all()
    return products_schema.jsonify(products)

@app.route('/orders', methods=['POST'])
def place_order():
    data = request.get_json()
    new_order = Order(date=datetime.utcnow(), customer_id=data['customer_id'])
    db.session.add(new_order)
    db.session.commit()
    
    for item in data['items']:
        order_item = OrderItem(order_id=new_order.id, product_id=item['product_id'], quantity=item['quantity'])
        db.session.add(order_item)
    
    db.session.commit()
    return order_schema.jsonify(new_order), 201

@app.route('/orders/<int:id>', methods=['GET'])
def retrieve_order(id):
    order = Order.query.get_or_404(id)
    return order_schema.jsonify(order)

@app.route('/orders/<int:id>/items', methods=['GET'])
def list_order_items(id):
    order_items = OrderItem.query.filter_by(order_id=id).all()
    return order_items_schema.jsonify(order_items)

@app.route('/orders/<int:id>/cancel', methods=['PUT'])
def cancel_order(id):
    order = Order.query.get_or_404(id)
    db.session.delete(order)
    db.session.commit()
    return jsonify({"message": "Order canceled successfully"})

@app.route('/orders/<int:id>/total', methods=['GET'])
def calculate_order_total(id):
    order_items = OrderItem.query.filter_by(order_id=id).all()
    total = sum(item.product.price * item.quantity for item in order_items)
    return jsonify({"total": total})

@app.route('/customers/<int:customer_id>/orders', methods=['GET'])
def manage_order_history(customer_id):
    orders = Order.query.filter_by(customer_id=customer_id).all()
    return orders_schema.jsonify(orders)
