from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# Add models here
class RestaurantPizza(db.Model, SerializerMixin):
    
    __tablename__ = 'restaurant_pizza'
    id = db.Column(db.Integer, primary_key=True)
    
    serialize_rules= ('-pizzas.restaurant', '-restaurants.pizza')
    price= db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizza.id'))

    
    @validates('price')
    def validates_price(self, key, price):
        if price < 0 and price < 30:
            raise AssertionError('Price must be greater than 0')
        return price
class Pizza(db.Model, SerializerMixin):
    __tablename__ = 'pizza'

    serialize_rules= ('-restaurants', '-restaurants_pizzas')
    
    
    id = db.Column(db.Integer, primary_key=True)
    
    name= db.Column(db.String)
    ingredients= db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    restaurant_pizzas = db.relationship('RestaurantPizza', backref = 'pizza')
    restaurants = association_proxy('restaurant_pizzas', 'restaurant')    
class Restaurant(db.Model, SerializerMixin):
    __tablename__ = 'restaurant'
    serialize_rules=  ('-pizzas', '-restaurant_pizza')
    
    id= db.Column(db.Integer, primary_key=True)
    
    name= db.Column(db.String)
    address= db.Column(db.String)
    
    restaurant_pizzas = db.relationship('RestaurantPizza', backref = 'restaurant')
    restaurants = association_proxy('restaurant_pizzas', 'pizza')