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


    @app.route('/cupcakes', methods=['POST'])
    def add_cupcake():
        print("add cupcake")
        if not request.json:
            abort(400)

        name = request.get_json()['name']
        description = request.get_json()['description']

        if name is None:
            abort(400)

        if description is None:
            description = ''

        new_cupcake = Cupcake(name=name, description=description)

        try:
            new_cupcake.insert()
        except DatabaseError:
            abort(422)

        return jsonify({'success': True}), 200


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

        return jsonify({'success': True}), 200


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