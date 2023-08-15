#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = []
    for bakery in Bakery.query.all():
        bakeries.append(bakery.to_dict())

    #Alternate solution 
    #bakeries = Bakery.query.all()
    #bakeries_serialized = [bakeries.to_dict() for bakery in bakeries]

    response = make_response(
        jsonify(bakeries),
        200
    )
    response.headers['Content-Type'] = 'application/json'
    return response 
    
@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter(Bakery.id == id).first()
    bakery_serialized = bakery.to_dict()

    response = make_response(
        jsonify(bakery_serialized),
        200
    )
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price_serialized = []
    for baked_good in BakedGood.query.order_by(BakedGood.price).all():
        baked_goods_by_price_serialized.append(baked_good.to_dict())

    response = make_response(
        jsonify(baked_goods_by_price_serialized),
        200
    )
    response.headers['Content-Type'] = 'application/json'
    return response

    #Alternate solution
    # baked_goods_by_price = BakedGood.query.order_by(BakedGood.price).all()
    # baked_goods_by_price_serialized = [bg.to_dict() for bg in baked_goods_by_price]

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive_serialized = (BakedGood.query.order_by(BakedGood.price.desc()).first()).to_dict()
    response = make_response(
        jsonify(most_expensive_serialized),
        200
    )
    response.headers['Content-Type'] = 'application/json'
    return response 

if __name__ == '__main__':
    app.run(port=5555, debug=True)
