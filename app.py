import os
from flask import Flask, request, jsonify, abort
from models import *
from flask_cors import CORS
import json
from sqlalchemy.exc import DatabaseError

def is_valid_cupcake(id):

    try:
        cupcakes = Cupcake.query.all()
    except DatabaseError:
        abort(422)

    cupcake_id_list = []
    for c in cupcakes:
        cupcake_id_list.append(c.id)

    if id in cupcake_id_list:
        return True
    else:
        return False

def attach_new_ingredients_to_cupcake(ingredients, the_cupcake):

    for i in ingredients:
        try:
            the_ingredient = Ingredient.query.filter_by(kind=i['kind']).filter_by(name=i['name']).one_or_none()
        except DatabaseError:
            print("unable to query ingredients")
            abort(422)
        if the_ingredient is None:
            # create the ingredient
            try:
                new_ingredient = Ingredient(name=i['name'], kind=i['kind'])
                new_ingredient.insert()
                the_cupcake.ingredients.append(new_ingredient)
            except DatabaseError:
                print("unable to create new ingredient")
                abort(422)
        else:
            the_cupcake.ingredients.append(the_ingredient)

        the_cupcake.update()


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

  
    @app.route('/')
    def get_greeting():
        # excited = os.environ['EXCITED']
        greeting = "Hello" 
        # if excited == 'true': greeting = greeting + "!!!!!"
        return greeting

    @app.route('/coolkids')
    def be_cool():
        return "Be cool, man, be coooool! You're almost a FSND grad!"

    @app.route('/cupcakes', methods=['GET'])
    def get_cupcakes():
        try:
            cupcakes = Cupcake.query.all()
        except DatabaseError:
            abort(422)

        print("cupcakes")
        clist = []
        for c in cupcakes:
            clist.append(c.long())

        return jsonify(clist), 200


    @app.route('/cupcakes/<int:id>')
    def get_cupcake_detail(id):

        if not is_valid_cupcake(id):
            abort(404)

        try:
            the_cupcake = Cupcake.query.filter_by(id=id).one_or_none()
        except DatabaseError:
            abort(422)

        if the_cupcake is None:
            abort(404)
        
        return jsonify({"success": True, "cupcake": the_cupcake.long()}), 200


# ---------------------------------------------------------------------------
#  Create a new cupcake with specified name and description.
#  If ingredients are included, check to see if they exist; if not, create
#  Associate the specified ingredients with the newly created cupcake.
# ---------------------------------------------------------------------------
    @app.route('/cupcakes', methods=['POST'])
    def add_cupcake():
        print("add cupcake")
        if not request.json:
            abort(400)

        name = request.get_json()['name']
        description = request.get_json()['description']
        ingredients = request.get_json()['ingredients']

        if name is None:
            abort(400)

        if description is None:
            description = ''

        # check if cupcake of specified name already exists
        try:
            the_cupcake = Cupcake.query.filter_by(name=name).one_or_none()
        except DatabaseError:
            print("error querying for existence of specified cupcake")
            abort(422)

        if the_cupcake is not None:
            print("a cupcake of the specified name already exists")
            abort(400)

        new_cupcake = Cupcake(name=name, description=description)

        if ingredients:
            attach_new_ingredients_to_cupcake(ingredients, new_cupcake)


        try:
            new_cupcake.insert()
        except DatabaseError:
            abort(422)

        return jsonify({'success': True, "cupcakes": new_cupcake.long()}), 200


# ---------------------------------------------------------------------------
#  Update the specified cupcake with specified name and description.
#  Cannot have optional ingredients, so ingredients will have to be 
#  specified. If ingredient list is not available, then the empty array 
#  should be specified.
# ---------------------------------------------------------------------------
    @app.route('/cupcakes/<int:id>', methods=['PATCH'])
    def update_cupcake(id):
        print ("update cupcake")

        if not request.json:
            abort(400)

        if not is_valid_cupcake(id):
            abort(404)

        the_cupcake = Cupcake.query.filter_by(id=id).one_or_none()

        name = request.get_json()['name']
        description = request.get_json()['description']
        ingredients = request.get_json()['ingredients']

        if name and name is not None:
            the_cupcake.name = name

        if description and description is not None:
            the_cupcake.description = description
        
        # remove ingredients from cupcake, then add them back
        the_cupcake.ingredients = []

        if ingredients:
            attach_new_ingredients_to_cupcake(ingredients, the_cupcake)
            # cupcake should get updated in attach_new_ingredients


        # try:
        #     the_cupcake.update()
        # except DatabaseError:
        #     print ("could not update the cupcake")
        #     abort(422)
    
        return jsonify({"success": True, "cupcake": the_cupcake.long()}), 200


    @app.route('/cupcakes/<int:id>', methods=['DELETE'])
    def delete_cupcake(id):
        print("delete cupcake")

        if not is_valid_cupcake(id):
            abort(404)
        
        try:
            the_cupcake = Cupcake.query.filter_by(id=id).one_or_none()
            the_cupcake.delete()
        except DatabaseError:
            print("Error occurred while trying to delete the cupcake")
            abort(422)

        return jsonify({"success": True, "delete": id}), 200

    @app.route('/ingredients')
    def get_ingredients():
        try:
            ingredients = Ingredient.query.all()
        except DatabaseError:
            abort(422)
        print("ingredients")
        ilist = []
        for i in ingredients:
            ilist.append(i.format())

        return jsonify(ilist)

    @app.route('/ingredients', methods=['POST'])
    def create_ingredient():

        print("create ingredient")
        if not request.json:
            abort(400)

        name = request.get_json()['name']
        kind = request.get_json()['kind']

        if name is None or kind is None:
            abort(400)

        new_ingredient = Ingredient(name=name, kind=kind)

        try:
            new_ingredient.insert()
        except DatabaseError:
            abort(422)

        return jsonify({'success': True,
                        'ingredients': new_ingredient.format()}), 200


    @app.route('/ingredients/<int:id>', methods=['PATCH'])
    def update_ingredient_name(id):
        if not request.json:
            abort(400)
            
        name = request.get_json()['name']
        kind = request.get_json()['kind']

        try:
            the_ingredient = Ingredient.query.filter_by(id=id).one_or_none()
        except DatabaseError:
            abort(422)

        if the_ingredient is None:
            abort(404)

        if name and name is not None:
            the_ingredient.name = name
        
        if kind and kind is not None:
            the_ingredient.kind = kind

        try:
            the_ingredient.update()
        except DatabaseError:
            print("unable to update the ingredient")
            abort(422)

        print("updated the ingredient")
        return jsonify({'success': True, "cupcake": the_ingredient.format()}), 200


    @app.errorhandler(422)
    def cannot_process(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Not processable"
        }), 422

    @app.errorhandler(404)
    def cannot_process(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404

    @app.errorhandler(400)
    def cannot_process(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"
        }), 400        

    return app

app = create_app()

if __name__ == '__main__':
    app.run()