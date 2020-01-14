
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
db = SQLAlchemy(app)


from models import *
from app import create_app
app = create_app()
app.app_context().push()


ingredients = Ingredient.query.all()

for i in ingredients:
    db.session.delete(i)

db.session.commit()

cupcakes = Cupcake.query.all()

for c in cupcakes:
    db.session.delete(c)
db.session.commit()    


ingredient1 = Ingredient(name="vanilla buttercream",
                         kind= "frosting")

ingredient2 = Ingredient(name="rainbow sprinkles",
                         kind="topping")

ingredient3 = Ingredient(name="yellow",
                         kind="cake")

ingredient4 = Ingredient(name="chocolate buttercream",
                         kind= "frosting")                         

db.session.add(ingredient1)
db.session.add(ingredient2)
db.session.add(ingredient3)

db.session.commit()


cupcake1 = Cupcake(name="Classic",
                   description="classic rich chocolate frosting on fluffy yellow cake")

cupcake2 = Cupcake(name="Chocolate Top to Bottom",
                   description="chocolate frosting on chocolate cake with chocolate chip topping")

cupcake1.ingredients.append(ingredient1)
ingredient1.usage_count = ingredient1.usage_count + 1
cupcake1.ingredients.append(ingredient2)
ingredient2.usage_count = ingredient2.usage_count + 1
cupcake1.ingredients.append(ingredient3)
ingredient3.usage_count = ingredient3.usage_count + 1

ingredient1.update()
ingredient2.update()
ingredient3.update()
db.session.add(cupcake1)
db.session.add(cupcake2)

db.session.commit()

# get new data 
cupcakes = Cupcake.query.all()
ingredients = Ingredient.query.all()
