#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Restaurant, RestaurantPizza, Pizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'



@app.route('/restaurants/', methods=['GET'])
def restaurants():
    if restaurant:
        restaurants = Restaurant.query.all()
        restaurants_dit = [restaurant.to_dict() for restaurant in restaurants]
        response= make_response(jsonify(restaurants_dit), 200)
    else:
        response= make_response(jsonify({'error': 'Restaurant not found'}), 404)
    
    return response

@app.route('/restaurants/<int:id>', methods=['GET'])
def restaurant(id):
    restaurant = Restaurant.query.filter(id == id).first()
    
    if restaurant:
        response = make_response(jsonify(restaurant.to_dict()), 200)
        
    else:
        response= make_response(jsonify({'error': 'Restaurant not found'}), 404)
        
    return response

@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.filter_by(id == id).first()
    
    if restaurant:
        db.session.delete(restaurant)
        db.session.commit()
        response = make_response(jsonify({'message': 'Restaurant deleted'}), 200)
    else:
        response = make_response(jsonify({'error': 'Restaurant not found'}), 404)
        
    return response


@app.route('/pizzas/', methods=['GET'])
def pizzas():
    pizzas = Pizza.query.all()
    pizzas_dict = [pizza.to_dict() for pizza in pizzas]
    response = make_response(jsonify(pizzas_dict), 200)
    
    return response


@app.route('/restaurant_pizzas/', methods=['POST'])
def restaurant_pizzas():
    
    restaurant_pizzas= restaurant_pizzas(
        pizza= request.get_json('pizza'),
        
        restaurant= request.get_json('restaurant'),
    )
    db.session.add(restaurant_pizzas)
    db.session.commit()
    
    response = make_response(jsonify(restaurant_pizzas.to_dict()), 201)
    
    return response
if __name__ == '__main__':
    app.run(port=5555, debug=True)
