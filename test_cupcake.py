import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy


from app import create_app
from models import Ingredient, setup_db, Cupcake, Order, OrderItem
# from models import Cupcake


chiefbaker_jwt = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJFUkZNRGN6TVRsRFFVWkZPRU0yUmprelFVVTFNRVUxUkRoRk1FTXpOVUUzUmpZMk9EQTRNdyJ9.eyJpc3MiOiJodHRwczovL3d1ZGV2LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZTJiNDcwNWIzMDNiNjBkYjYwN2I1ZTciLCJhdWQiOiJjdXBjYWtlY2FmZSIsImlhdCI6MTU3OTk5MTc4NCwiZXhwIjoxNTc5OTk4OTg0LCJhenAiOiJlZTlyWENBR0RFY1JNZGZmclZkMjZibFU5UExxZGdrNSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmN1cGNha2VzIiwiZGVsZXRlOmluZ3JlZGllbnRzIiwiZ2V0OmN1cGNha2VzIiwiZ2V0OmluZ3JlZGllbnRzIiwicGF0Y2g6Y3VwY2FrZXMiLCJwYXRjaDppbmdyZWRpZW50cyIsInBvc3Q6Y3VwY2FrZXMiLCJwb3N0OmluZ3JlZGllbnRzIl19.Jo8JTzFuldk8k-ict9e0zy--vkw3RNWcbYpCFhWsM5SkLUg_NBxiaFyqmK6JboPLZA_0uR-BFLKNpAIt6kaVrITMoHS_rcUy1VgypPUUg1epNgkMTkkPrxKj01HK6w19ElR6ZRGd1BVefnxV6KFW7zP8-qTWcAJBkX6wDmenAdoDehKBvQwDq9Xig9p_NF0-PWrTWWNjKd6vLAFX-ixNqIYOGy_wyuoNqf1DeUX13PWlYsRmbJcLh6K4wExH2yj3z0j5xYOt_T34t2ShBiq1PQweozsnjVSd895FyM8dL-ZM8RnxUonu3e51uKT6kX91kOda1eQYg5DWlY64f5n5UA'
bakerymanager_jwt = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJFUkZNRGN6TVRsRFFVWkZPRU0yUmprelFVVTFNRVUxUkRoRk1FTXpOVUUzUmpZMk9EQTRNdyJ9.eyJpc3MiOiJodHRwczovL3d1ZGV2LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZTJiNDc4MmNjMmRhODBlOTgxM2YzNTciLCJhdWQiOiJjdXBjYWtlY2FmZSIsImlhdCI6MTU3OTk5MzMwNiwiZXhwIjoxNTgwMDAwNTA2LCJhenAiOiJlZTlyWENBR0RFY1JNZGZmclZkMjZibFU5UExxZGdrNSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOm9yZGVycyIsImdldDppbmdyZWRpZW50cyIsImdldDpvcmRlcnMiLCJwYXRjaDpvcmRlcnMiLCJwb3N0Om9yZGVycyJdfQ.RY3-UntopwjhfsPX9xGkPg7NE0RiTUXU-ePWapfI7RLAUYAz8xewanrQDd0o3Ir5liGa7pePUCPmShsd8fxxZneHEn-I6XvSiVk2qEuH-5-W4W5evBzIhClbmgiebEQAZChtml3osKlIylseKkqJpGUD7C_tGcd7WY72PSPfNNHQTqH6UAu5NjSCBwo1R8tb4m6wuw0OfA2O1f1ntrrnxn7srBFQbjg548CtUEJa6R_BDg77GRwSO85VqgNxUsRXw3g6n11y87AVNpBuqM5PSXpl52rGQbfmNiBbtQKgm4jIB9Zxu-Lfz0tmQ27trEz6aYvAHVZPPPaQtgFfZk0hdw'
bakeryclerk_jwt = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJFUkZNRGN6TVRsRFFVWkZPRU0yUmprelFVVTFNRVUxUkRoRk1FTXpOVUUzUmpZMk9EQTRNdyJ9.eyJpc3MiOiJodHRwczovL3d1ZGV2LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZTJiNDdjZjRlMjdmZDBmMDM1ZWFlNjIiLCJhdWQiOiJjdXBjYWtlY2FmZSIsImlhdCI6MTU3OTk5NTc2NSwiZXhwIjoxNTgwMDAyOTY1LCJhenAiOiJlZTlyWENBR0RFY1JNZGZmclZkMjZibFU5UExxZGdrNSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmN1cGNha2VzIiwiZ2V0Om9yZGVycyJdfQ.q7HxirwpSvnOsQE_vuvNRtQqrRvg9v0F7xudzJGu8l46DQ8dys0likrykDp6VVVWnEAiUbgcWhXDXQs7kvo9yINja6dvmamNY9dPpiSuMN95xou4wZKrUKQ_-TOQeXUhgO6yIn5GhdBpgiaYJk0PVGT94-N-k2X2HnfJ_51QXycRtNFghm6gtXuvRIJl3njLHAqfxuTh4700gukkQeBEVlQOeEipjO9DDqOymobELQCNtmnZxO-moYFC9FaEtS5Wya8psnzXI0t99FJHM7dmcwRHEo6hIsD0Wu5LBqylPjfii0-7mhfTmKQo9awhyTs6tG8YpfOLCE-Bze0ZAOsoAQ'

class CupcakeTests(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "cupcakecafe_test"
        self.database_path = (
            "postgres://{}/{}"
            .format('localhost:5432', self.database_name)
        )
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # ----------------------------------------------------------------------------
    #  GET /cupcakes
    # ----------------------------------------------------------------------------
    def test_get_cupcakes(self):
        print ("test GET cupcakes")
        res = self.client().get('/cupcakes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['cupcakes'])


    # test PUT /cupcakes
        print ("test PUT cupcakes")
        res = self.client().put('/cupcakes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)


    # ----------------------------------------------------------------------------
    #  GET /cupcakes/<int:id>
    # ----------------------------------------------------------------------------    
    def test_get_specific_cupcake(self):
        print ("test GET specific cupcake")
        res = self.client().get('/cupcakes/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['cupcakes'])

    # test getting a non-existent cupcake returns 404
    def test_get_non_existent_cupcake(self):
        print ("test GET non-existent cupcake returns 404")
        res = self.client().get('/cupcakes/999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)


    # ----------------------------------------------------------------------------
    #  POST /cupcakes
    # ----------------------------------------------------------------------------  
    def test_create_cupcake(self):
        print("test POST /cupcakes with chiefbaker jwt")

        headers = {
            'Authorization': 'Bearer {}'.format(chiefbaker_jwt)
        }
        res = (
            self.client()
                .post('/cupcakes', headers=headers,
                      json={'name': 'New Cupcake',
                            'description': 'description of New Cupcake',
                            'ingredients': [{'kind': 'topping', 'name': 'new topping'}]
                      })
        )
        data = json.loads(res.data)
        # verify that it was created in the database
        the_cupcake = (Cupcake.query
                              .filter_by(name='New Cupcake')  
                              .filter_by(description='description of New Cupcake')
                              .first()
        )
        self.assertTrue(the_cupcake is not None)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['cupcakes'])


    # ----------------------------------------------------------------------------
    #   POST /cupcakes (bad data)
    #       kind is missing from ingredients list    
    #       returns 400, bad request:
    # ----------------------------------------------------------------------------
    def test_create_cupcake_faulty_input(self):
        print("test POST /cupcakes faulty input with chiefbaker jwt")

        headers = {
            'Authorization': 'Bearer {}'.format(chiefbaker_jwt)
        }        
        res = (
            self.client()
                .post('/cupcakes', headers=headers,
                      json={'name': 'New Cupcake Faulty',
                            'description': 'description of New Cupcake Faulty',
                            'ingredients': [{'name': 'new topping for faulty cupcake'}]
                      })
        )
        data = json.loads(res.data)
        # verify that it was not created in the database
        the_cupcake = (Cupcake.query
                              .filter_by(name='New Cupcake Faulty')  
                              .filter_by(description='description of New Cupcake Faulty')
                              .one_or_none()
        )
        self.assertTrue(the_cupcake is None)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)



    # ----------------------------------------------------------------------------
    #   POST /cupcakes (bad data)
    #       name is missing from Cupcake
    #       returns 400, bad request:
    # ----------------------------------------------------------------------------
    def test_create_cupcake_faulty_input(self):
        print ("test create cupcake with faulty input, no name specified for cupcake")

        headers = {
            'Authorization': 'Bearer {}'.format(chiefbaker_jwt)
        }                
        res = (
            self.client()
                .post('/cupcakes', headers=headers,
                      json={'description': 'description of New Cupcake Faulty Name Missing',                            
                            'ingredients': [{'kind': 'topping', 'name': 'new topping for faulty cupcake'}]
                      })
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    # ----------------------------------------------------------------------------
    #   DELETE /cupcakes
    # ----------------------------------------------------------------------------
    def test_delete_cupcake(self):
        print("test deleting a cupcake")

        headers = {
            'Authorization': 'Bearer {}'.format(chiefbaker_jwt)
        }   
        res = self.client().delete('/cupcakes/2', headers=headers)
        data = json.loads(res.data)

        cupcake = Cupcake.query.filter(Cupcake.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(cupcake, None)


    # ----------------------------------------------------------------------------
    #   DELETE /cupcakes
    #        a non-existent cupcake returns 404
    # ----------------------------------------------------------------------------
    def test_delete_non_existent_cupcake(self):
        print("test deleting a non-existent cupcake")
        headers = {
            'Authorization': 'Bearer {}'.format(chiefbaker_jwt)
        }   

        res = self.client().delete('/cupcakes/222', headers=headers)
        data = json.loads(res.data)


        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)


    # ----------------------------------------------------------------------------
    #   PATCH /cupcakes/<int:id>
    #       change specified cupcake's name and description
    # ----------------------------------------------------------------------------
    def test_update_cupcake(self):
        print("testing updating a cupcake")
        headers = {
            'Authorization': 'Bearer {}'.format(chiefbaker_jwt)
        }           
        res = self.client().patch('/cupcakes/3', headers=headers,
                                  json = {"name": "change of name", "description": "new description", "ingredients": [] })

        data = json.loads(res.data)
        the_cupcake = (Cupcake.query
                              .filter(Cupcake.id==3)
                              .first()
        )
        self.assertEqual(the_cupcake.short()['name'], 'change of name')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    # ----------------------------------------------------------------------------
    #   PATCH /cupcakes/<int:id>
    #       updating a non-existent cupcake results in 404
    # ----------------------------------------------------------------------------
    def test_update_non_existent_cupcake(self):
        print("test updating a non-existent cupcake")
        headers = {
            'Authorization': 'Bearer {}'.format(chiefbaker_jwt)
        }    

        res = self.client().patch('/cupcakes/300', headers=headers,
                                  json = {"name": "change of name", "description": "new description", "ingredients": [] })

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)                                  



    # ----------------------------------------------------------------------------
    #   GET /orders
    # ----------------------------------------------------------------------------
    def test_get_orders(self):
        print ("test GET orders")
        headers = {
            'Authorization': 'Bearer {}'.format(bakerymanager_jwt)
        }    

        res = self.client().get('/orders', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['orders'])        
        self.assertEqual(data['success'], True)

    # ----------------------------------------------------------------------------
    #   GET /orders
    #      wrong permissions
    # ----------------------------------------------------------------------------
    def test_get_orders_with_wrong_permissions(self):
        print ("test GET orders with wrong permissions")
        headers = {
            'Authorization': 'Bearer {}'.format(chiefbaker_jwt)
        }    

        res = self.client().get('/orders', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)     
        self.assertEqual(data['success'], False)


    # ----------------------------------------------------------------------------
    #   GET /orders/<int:id>
    # ----------------------------------------------------------------------------        
    def test_get_specific_order(self):
        print ("test GET specific order")

        headers = {
            'Authorization': 'Bearer {}'.format(bakerymanager_jwt)
        }            
        res = self.client().get('/orders/1', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['orders'])        
        self.assertEqual(data['success'], True)


    # ----------------------------------------------------------------------------
    #   GET /orders/<int:id>
    #        getting a non-existent order returns 404    
    # ----------------------------------------------------------------------------     
    def test_get_non_existent_order(self):
        print ("test GET non-existent order returns 404")
        headers = {
            'Authorization': 'Bearer {}'.format(bakerymanager_jwt)
        }             
        res = self.client().get('/orders/999', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)


    # ----------------------------------------------------------------------------
    #   DELETE /orders/<int:id>
    # ----------------------------------------------------------------------------
    def test_delete_order(self):
        print("test DELETE specified order")

        headers = {
            'Authorization': 'Bearer {}'.format(bakerymanager_jwt)
        }   
        res = self.client().delete('/orders/2', headers=headers)
        data = json.loads(res.data)

        the_order = Order.query.filter_by(id=6).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(the_order, None)


    # ----------------------------------------------------------------------------
    #   DELETE /orders/<int:id>
    #       delete non-existent order
    # ----------------------------------------------------------------------------
    def test_delete_non_existent_order(self):
        print ("test DELETE non-existent order")
        headers = {
            'Authorization': 'Bearer {}'.format(bakerymanager_jwt)
        }           
        res = self.client().delete('/orders/555', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)       

    # ----------------------------------------------------------------------------
    #   POST /orders
    # ----------------------------------------------------------------------------
    def test_create_order(self):
        print("test POST orders")
        headers = {
            'Authorization': 'Bearer {}'.format(bakerymanager_jwt)
        }            
        res = (
            self.client()
                .post('/orders', headers=headers,
                      json={'customer_name': 'New Order',
                            'order_items': [{'cupcake_id': 1, 'quantity': 30}]
                      })
        )
        data = json.loads(res.data)
        # verify that it was created in the database
        the_order = (Order.query
                          .filter_by(customer_name='New Order')  
                          .first()
        )
        the_order_item = (OrderItem.query
                                   .filter_by(cupcake_id=1)
                                   .filter_by(quantity=30)
        )

        self.assertTrue(the_order is not None)
        self.assertTrue(the_order_item is not None)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['orders'])


    # ----------------------------------------------------------------------------
    #   POST /orders
    #       bad cupcake id: can't order a cupcake that doesn't exist
    # ----------------------------------------------------------------------------
    def test_create_order_with_bad_data(self):
        print("create order with bad cupcake id")
        headers = {
            'Authorization': 'Bearer {}'.format(bakerymanager_jwt)
        }             
        res = (
            self.client()
                .post('/orders', headers=headers,
                      json={'customer_name': 'New Order',
                            'order_items': [{'cupcake_id': 901, 'quantity': 30}]
                      })
        )
        data = json.loads(res.data)        
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)



    # ----------------------------------------------------------------------------
    #   POST /orders
    #       improperly specified order_items: missing quantity
    # ----------------------------------------------------------------------------
    def test_create_order_with_bad_data2(self):
        print("test create order with no quantity specified")
        headers = {
            'Authorization': 'Bearer {}'.format(bakerymanager_jwt)
        }           
        res = (
            self.client()
                .post('/orders', headers=headers,
                      json={'customer_name': 'New Order',
                            'order_items': [{'cupcake_id': 14}]
                      })
        )
        data = json.loads(res.data)        
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)   


    # ----------------------------------------------------------------------------
    #   PATCH /orders
    # ----------------------------------------------------------------------------
    def test_update_order(self):
        print("test PATCH orders")
        headers = {
            'Authorization': 'Bearer {}'.format(bakerymanager_jwt)
        }           
        res = self.client().patch('/orders/1', headers=headers,
                                  json = {"customer_name": "Mr. Customer", "order_items": [{'cupcake_id': 1, 'quantity': 10}]})

        data = json.loads(res.data)
        the_order = (Order.query
                          .filter(Order.id==1)
                          .first()
        )
        the_order_item = (OrderItem.query
                                   .filter_by(order_id=the_order.id).one_or_none
        )
        self.assertEqual(the_order.format()['customer_name'], 'Mr. Customer')
        self.assertTrue(the_order_item)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)    


    # ----------------------------------------------------------------------------
    #   PATCH /orders/<int:id>
    #      attempt to update non-existent order
    # ----------------------------------------------------------------------------
    def test_update_order_non_existent(self):
        print("test update of non-existent order")
        headers = {
            'Authorization': 'Bearer {}'.format(bakerymanager_jwt)
        }            
        res = self.client().patch('/orders/120', headers=headers,
                                  json = {"customer_name": "Mr. Customer", "order_items": [{'cupcake_id': 14, 'quantity': 10}]})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)   


    # ----------------------------------------------------------------------------
    #   PATCH /orders/<int:id>
    #      invalid data: no customer name specified
    # ----------------------------------------------------------------------------
    def test_update_order_bad_data(self):
        print("test PATCH order with no customer name specified")

        headers = {
            'Authorization': 'Bearer {}'.format(bakerymanager_jwt)
        }            
        res = self.client().patch('/orders/120', headers=headers,
                                  json = {"order_items": [{'cupcake_id': 1, 'quantity': 10}]})

        data = json.loads(res.data)        

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)    


    # ----------------------------------------------------------------------------
    #  GET /ingredients
    # ----------------------------------------------------------------------------
    def test_get_ingredients(self):
        print ("test GET ingredients")
        headers = {
            'Authorization': 'Bearer {}'.format(bakerymanager_jwt)
        }               
        res = self.client().get('/ingredients', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['ingredients'])

    # ----------------------------------------------------------------------------
    #  GET /ingredients
    #      no authorization
    # ----------------------------------------------------------------------------
    def test_get_ingredients_wrong_permissions(self):
        print ("test GET ingredients with wrong permissions")
          
        headers = {
            'Authorization': 'Bearer {}'.format(bakeryclerk_jwt)
        }                
        res = self.client().get('/ingredients', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
       

    # ----------------------------------------------------------------------------
    #  POST /ingredients
    # ----------------------------------------------------------------------------
    def test_post_ingredients(self):
        print("test create ingredients")
        headers = {
            'Authorization': 'Bearer {}'.format(chiefbaker_jwt)
        }           
        res = (
            self.client()
                .post('/ingredients', headers=headers,
                      json={'name': 'New Frosting',
                            'kind': 'frosting'
                      })
        )

        data = json.loads(res.data)
        # verify that it was created in the database
        the_ingredient = (Ingredient.query
                                    .filter_by(name='New Frosting')  
                                    .filter_by(kind='frosting')
                                    .first()
        )
        self.assertTrue(the_ingredient is not None)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['ingredients'])

    # ----------------------------------------------------------------------------
    #  POST /ingredients
    #     missing kind of ingredient
    # ----------------------------------------------------------------------------
    def test_post_ingredients_bad_data(self):
        print("test create ingredients")
        headers = {
            'Authorization': 'Bearer {}'.format(chiefbaker_jwt)
        }           
        res = (
            self.client()
                .post('/ingredients', headers=headers,
                      json={'name': 'New Frosting 2',
                      })
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    # ----------------------------------------------------------------------------
    #  DELETE /ingredients/<int:id>
    # ----------------------------------------------------------------------------
    def test_delete_ingredient(self):
        print("test DELETE specified ingredient")

        headers = {
            'Authorization': 'Bearer {}'.format(chiefbaker_jwt)
        }   
        res = self.client().delete('/ingredients/2', headers=headers)
        data = json.loads(res.data)

        the_ingredient = Ingredient.query.filter_by(id=2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(the_ingredient, None)


    # ----------------------------------------------------------------------------
    #  DELETE /ingredients/<int:id>
    #      ingredient does not exist
    # ----------------------------------------------------------------------------
    def test_delete_ingredient_non_existent(self):
        print("test DELETE non-existent ingredient")

        headers = {
            'Authorization': 'Bearer {}'.format(chiefbaker_jwt)
        }   
        res = self.client().delete('/ingredients/2000', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    # ----------------------------------------------------------------------------
    #  PATCH /ingredients/<int:id>
    # ----------------------------------------------------------------------------
    def test_patch_ingredients(self):
        print("testing updating an ingredient")
        headers = {
            'Authorization': 'Bearer {}'.format(chiefbaker_jwt)
        }           
        res = self.client().patch('/ingredients/4', headers=headers,
                                  json = {"name": "chocolate sprinkles", "kind": "topping" })

        data = json.loads(res.data)
        the_ingredient = (Ingredient.query
                                    .filter(Ingredient.id==4)
                                    .first()
        )
        self.assertEqual(the_ingredient.format()['name'], 'chocolate sprinkles')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    # ----------------------------------------------------------------------------
    #  PATCH /ingredients/<int:id>
    #     ingredient does not exist
    # ----------------------------------------------------------------------------
    def test_patch_ingredients(self):
        print("testing updating a non-existent ingredient")
        headers = {
            'Authorization': 'Bearer {}'.format(chiefbaker_jwt)
        }           
        res = self.client().patch('/ingredients/4000', headers=headers,
                                  json = {"name": "chocolate sprinkles", "kind": "topping" })

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)        

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()