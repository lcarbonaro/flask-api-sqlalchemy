# imports
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

# initialise flask app
app = Flask(__name__)

# app db config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# MODELS

class Product(db.Model,SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)  
    desc = db.Column(db.String(50))
    reviews = db.relationship('Review', backref='product')

    serialize_rules = ('-reviews.product' ,)

class Buyer(db.Model,SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)  
    name = db.Column(db.String(50))
    reviews = db.relationship('Review', backref='buyer')
    
    serialize_rules = ('-reviews.buyer' ,)

class Review(db.Model,SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)  
    comment = db.Column(db.String(100))  
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    buyer_id = db.Column(db.Integer, db.ForeignKey('buyer.id'))

    serialize_rules = ('-product.reviews' , '-buyer.reviews')


# buyer buys many products
# products are bought by many buyers
# so many-to-many needs join table
# how used??
buyer_product = db.Table('buyer_product',
    db.Column('buyer_id', db.Integer, db.ForeignKey('buyer.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
)


# ROUTES / ENDPOINTS
# test route
@app.route('/test', methods=['GET'])
def test():
    return {"hello": "world"}

# get all products
@app.route('/product', methods=['GET'])
def get_products():
    all_products = Product.query.all()
    return [ product.to_dict() for product in all_products ] # list 

# add a new product
@app.route('/product', methods=['POST'])
def add_product():
    prod_desc = request.json['prod_desc']
    new_product = Product(desc=prod_desc)
    db.session.add(new_product)
    db.session.commit()
    return new_product.to_dict()

# get all buyers
@app.route('/buyer', methods=['GET'])
def get_buyers():
    all_buyers = Buyer.query.all()
    return [ buyer.to_dict() for buyer in all_buyers ]



# get one product by id
@app.route('/product/<prod_id>', methods=['GET'])
def get_product(prod_id):
    product = Product.query.get(prod_id)
    return product.to_dict()

# get one buyer by id
@app.route('/buyer/<buyer_id>', methods=['GET'])
def get_buyer(buyer_id):
    buyer = Buyer.query.get(buyer_id)
    return buyer.to_dict()




# start flask server
if __name__ == '__main__':
    app.run(debug=True)
