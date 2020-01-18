import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Person
Have title and release year
'''
# class Person(db.Model):  
#   __tablename__ = 'People'

#   id = Column(Integer, primary_key=True)
#   name = Column(String)
#   catchphrase = Column(String)

#   def __init__(self, name, catchphrase=""):
#     self.name = name
#     self.catchphrase = catchphrase

#   def format(self):
#     return {
#       'id': self.id,
#       'name': self.name,
#       'catchphrase': self.catchphrase}

cupcake_ingredient = db.Table('cupcake_ingredient',
    db.Column('cupcake_id', db.Integer, db.ForeignKey('Cupcake.id')),
    db.Column('ingredient_id', db.Integer, db.ForeignKey('Ingredient.id'))
)

class Cupcake(db.Model):
  __tablename__ = 'Cupcake'

  id = Column(Integer, primary_key=True)
  name = Column(String, nullable=False, unique=True)
  description = Column(String)
  ingredients = db.relationship('Ingredient', secondary=cupcake_ingredient,
                                              backref=db.backref('cupcakes'), lazy=True)
  order_items = db.relationship('OrderItem', backref=db.backref('cupcake'), lazy=True)                                              


  def short(self):
      return {
        'id': self.id,
        'name': self.name,
        'description': self.description
      }


  def long(self):
      ilist = []
      for i in self.ingredients:
        ilist.append(
          {'name': i.name,
          'kind': i.kind}
        )
      return {
        'id': self.id,
        'name': self.name,
        'description': self.description,
        'ingredients': ilist
      }

  def insert(self):
      db.session.add(self)
      db.session.commit()

  def delete(self):
      db.session.delete(self)
      db.session.commit()

  def update(self):
      db.session.commit()

  def __repr__(self):
      return f'<Cupcake {self.id}, {self.name}>'      

class Ingredient(db.Model):
    __tablename__ = 'Ingredient'

    id = Column(Integer, primary_key=True)
    kind = Column(String, nullable=False)
    name = Column(String, nullable=False, unique=True)
    usage_count = Column(Integer, default=0)

    def format(self):
        return {
          'id': self.id,
          'kind': self.kind,
          'name': self.name,
          'usage_count': self.usage_count}

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
        return f'<Ingredient {self.id}, {self.name}>'

class Order(db.Model):
    __tablename__ = 'Order'

    id = Column(Integer, primary_key=True)
    customer_name = Column(String, nullable=False)
    order_items = db.relationship('OrderItem', cascade="all,delete", backref=db.backref('order'), lazy=True)

    def format(self):

        order_item_list = []
        for oi in self.order_items:
            order_item_list.append(
                {'cupcake_id': oi.cupcake_id,
                 'cupcake_name': oi.cupcake.name,
                 'quantity': oi.quantity}
            )

        return {
          'id': self.id,
          'customer_name': self.customer_name,
          'order_items': order_item_list
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()
        
class OrderItem(db.Model):
    __tablename__ = 'OrderItem'

    id = Column(Integer, primary_key=True)
    cupcake_id = db.Column(db.Integer, db.ForeignKey('Cupcake.id'))
    quantity = db.Column(db.Integer, default=0)
    order_id = db.Column(db.Integer, db.ForeignKey('Order.id'))

    def format(self):
        return {
          'id': self.id,
          'cupcake_id': self.cupcake_id,
          'quantity': self.quantity,
          'order_id': self.order_id
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()        
                    
    def __repr__(self):
        return f'<OrderItem {self.id}, {self.cupcake_id}, {self.quantity}>'
