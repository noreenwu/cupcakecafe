import os
from flask import Flask, request, jsonify, abort
from models import *
from flask_cors import CORS
import json
from sqlalchemy.exc import DatabaseError

# def is_valid_cupcake(id):

#     try:
#         cupcakes = Cupcake.query.all()
#     except DatabaseError:
#         abort(422)

#     cupcake_id_list = []
#     for c in cupcakes:
#         cupcake_id_list.append(c.id)

#     if id in cupcake_id_list:
#         return True
#     else:
#         return False

# -----------------------------------------------------------------------------------
#  Since the specified cupcake is about to have its ingredients reset, first
#  update the usage_counts of the ingredients that it will no longer be associated
#  with.
# -----------------------------------------------------------------------------------
def update_ingredient_usage_counts(the_cupcake):

    for i in the_cupcake.ingredients:
        if i.usage_count > 0:
            i.usage_count = i.usage_count - 1
        try:
            i.update()
        except DatabaseError:
            print("unable to update ingredient usage_count")
            abort(422)


def attach_new_ingredients_to_cupcake(ingredients, the_cupcake):

    for i in ingredients:
        try:
            i['name']
            i['kind']
        except KeyError:
            print("could not get name or kind of ingredient from input")
            abort(400)        
        try:
            the_ingredient = Ingredient.query.filter_by(kind=i['kind']).filter_by(name=i['name']).one_or_none()
        except DatabaseError:
            print("unable to query ingredients")
            abort(422)
        if the_ingredient is None:
            # create the ingredient
            try:
                new_ingredient = Ingredient(name=i['name'], kind=i['kind'], usage_count=1)
                new_ingredient.insert()
                the_cupcake.ingredients.append(new_ingredient)
            except DatabaseError:
                print("unable to create new ingredient")
                abort(422)
        else:
            the_cupcake.ingredients.append(the_ingredient)
            the_ingredient.usage_count = the_ingredient.usage_count + 1
            try:
                the_ingredient.update()
            except DatabaseError:
                print("unable to update ingredient")
                abort(422)

        the_cupcake.update()


def get_order_items_db(order_items, order_id):
    orders_db_form = []

    for o in order_items:
        try:
            cc_id = o['cupcake_id']
            quant = o['quantity']
            print("cupcake id was ", cc_id)
            print("quantity specified was ", quant)
            print("and the order id was ", order_id)
        except KeyError:
            print("could not get cupcake_id or quantity from input")
            abort(400)

        # ensure that the specified cupcake id actually exists
        try:
            valid_cupcake = Cupcake.query.filter_by(id=cc_id).one_or_none()
        except DatabaseError:
            abort(422)

        if valid_cupcake is None:  # specified cupcake doesn't exist
            abort(400)

        try:
            new_order_item = OrderItem(cupcake_id=cc_id, quantity=quant, order_id=order_id)
            new_order_item.insert()

        except DatabaseError:
            print("could not insert new order item")
            abort(422)

        orders_db_form.append(new_order_item)

    return (orders_db_form)
    

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

  
    # @app.route('/')
    # def get_greeting():
    #     # excited = os.environ['EXCITED']
    #     greeting = "Hello" 
    #     # if excited == 'true': greeting = greeting + "!!!!!"
    #     return greeting

    # @app.route('/coolkids')
    # def be_cool():
    #     return "Be cool, man, be coooool! You're almost a FSND grad!"

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

        return jsonify({"success": True, "cupcakes": clist}), 200


    @app.route('/cupcakes/<int:id>')
    def get_cupcake_detail(id):

        try:
            the_cupcake = Cupcake.query.filter_by(id=id).one_or_none()
        except DatabaseError:
            abort(422)

        if the_cupcake is None:
            abort(404)
        clist = []
        clist.append(the_cupcake.long())
        return jsonify({"success": True, "cupcakes": clist}), 200


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

        try:
            name = request.get_json()['name']
            description = request.get_json()['description']
            ingredients = request.get_json()['ingredients']
        except KeyError:
            print("could not get name, description or ingredients from input")
            abort(400)

        if not name or name is None:
            abort(400)

        if not description or description is None:
            description = ''

        if not ingredients or ingredients is None:
            ingredients = []

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

        # if not is_valid_cupcake(id):
        #     abort(404)

        try:
            the_cupcake = Cupcake.query.filter_by(id=id).one_or_none()
        except DatabaseError:
            print("unable to query database")
            abort(422)

        if the_cupcake is None:
            abort(404)

        try:
            name = request.get_json()['name']
            description = request.get_json()['description']
            ingredients = request.get_json()['ingredients']
        except KeyError:
            abort(400)

        if name and name is not None:
            # check if new name is already taken
            try:
                cc_same_name = Cupcake.query.filter_by(name=name).filter(id!=the_cupcake.id).one_or_none()
            except DatabaseError:
                abort(422)
            if cc_same_name is not None:
                print("a cupcake of same name already exists")
                abort(400)
            the_cupcake.name = name

        if description and description is not None:
            the_cupcake.description = description        

        # if no ingredients are specified, usage_counts are updated and cupcake's ingredients are reset
        update_ingredient_usage_counts(the_cupcake)
        the_cupcake.ingredients = []    # remove any old ingredients   
        if ingredients:    
            attach_new_ingredients_to_cupcake(ingredients, the_cupcake)
            # cupcake should get updated in attach_new_ingredients


        # try:
        #     the_cupcake.update()
        # except DatabaseError:
        #     print ("could not update the cupcake")
        #     abort(422)
        clist = [the_cupcake.long()]
        
        return jsonify({"success": True, "cupcakes": clist }), 200


    @app.route('/cupcakes/<int:id>', methods=['DELETE'])
    def delete_cupcake(id):
        print("delete cupcake")
        
        try:
            the_cupcake = Cupcake.query.filter_by(id=id).one_or_none()
            if the_cupcake is None:
                abort(404)
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

        try:
            name = request.get_json()['name']
            kind = request.get_json()['kind']
        except KeyError:
            print("could not get values name or kind from input")
            abort(400)

        if not name or name is None or not kind or kind is None:
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
            
        try:
            name = request.get_json()['name']
            kind = request.get_json()['kind']
        except KeyError:
            print("could not get values name or kind from input")
            abort(400)

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


    # orders
    @app.route('/orders', methods=['GET'])
    def get_orders():
        try:
            orders = Order.query.all()
        except DatabaseError:
            abort(422)

        print("orders")
        order_list = []
        for o in orders:
            order_list.append(o.format())

        return jsonify({"success": True, "orders": order_list}), 200

    # get a specific order
    @app.route('/orders/<int:id>', methods=['GET'])
    def get_orders_detail(id):

        try:
            the_order = Order.query.filter_by(id=id).one_or_none()
        except DatabaseError:
            abort(422)

        if the_order is None:
            abort(404)
        orderlist = [the_order.format()]
        return jsonify({"success": True, "orders": orderlist}), 200


    @app.route('/orders/<int:id>', methods=['DELETE'])
    def delete_order(id):
        print("delete order")
        
        try:
            the_order = Order.query.filter_by(id=id).one_or_none()
            if the_order is None:
                abort(404)
            the_order.delete()  # should cascade delete all associated OrderItems
        except DatabaseError:
            print("Error occurred while trying to delete the cupcake")
            abort(422)

        return jsonify({"success": True, "delete": id}), 200


    @app.route('/orders', methods=['POST'])
    def create_order():

        print("create order")
        if not request.json:
            abort(400)

        try:
            customer_name = request.get_json()['customer_name']
            order_items = request.get_json()['order_items']
        except KeyError:
            print("could not get values customer_name or order_values from input")
            abort(400)

        if not customer_name or customer_name is None or not order_items or order_items is None:
            abort(400)

        try:
            new_order = Order(customer_name=customer_name)  # add order_items after; they need the order_id
            new_order.insert()
        except DatabaseError:
            print("could not insert new order")
            abort(422)
            

        db_order_items = get_order_items_db(order_items, new_order.id)
        if len(db_order_items) == 0:
            print("no order items for this order")
            abort(400)

        return jsonify({'success': True,
                        'orders': new_order.format()}), 200


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