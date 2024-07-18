from . import db, ma

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    accounts = db.relationship('CustomerAccount', backref='customer', lazy=True)
    orders = db.relationship('Order', backref='customer', lazy=True)

class CustomerAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    order_items = db.relationship('OrderItem', backref='product', lazy=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    items = db.relationship('OrderItem', backref='order', lazy=True)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        include_relationships = True
        load_instance = True

class CustomerAccountSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CustomerAccount
        include_relationships = True
        load_instance = True

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        include_relationships = True
        load_instance = True

class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        include_relationships = True
        load_instance = True

class OrderItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = OrderItem
        include_relationships = True
        load_instance = True
