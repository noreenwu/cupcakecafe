import os
from flask import Flask, jsonify
from models import *
from flask_cors import CORS
import json
from sqlalchemy.exc import DatabaseError

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

    @app.route('/cupcakes')
    def get_cupcakes():
        try:
            cupcakes = Cupcake.query.all()
        except DatabaseError:
            abort(422)

        print("cupcakes")
        clist = []
        for c in cupcakes:
            clist.append(c.format())

        return jsonify(clist)


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
        

    @app.errorhandler(422)
    def cannot_process(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Not processable"
        }), 422

    return app

app = create_app()

if __name__ == '__main__':
    app.run()