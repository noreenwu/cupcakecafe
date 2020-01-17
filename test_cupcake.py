import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy


from app import create_app
from models import Ingredient, setup_db
from models import Cupcake


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

    # test getting cupcakes
    def test_get_cupcakes(self):
        print ("test GET cupcakes")
        res = self.client().get('/cupcakes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['cupcakes'])

    # test getting specific cupcake
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
        res = self.client().get('cupcakes/999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)


    # test creation of new cupcake
    def test_create_cupcake(self):
        res = (
            self.client()
                .post('/cupcakes',
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


    # test creation of new cupcake with faulty input returns 400, bad request:
    #   kind is missing from ingredients list
    def test_create_cupcake_faulty_input(self):
        res = (
            self.client()
                .post('/cupcakes',
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


    # test creation of new cupcake with faulty input returns 400, bad request:
    #   name is missing
    def test_create_cupcake_faulty_input(self):
        print ("test create cupcake with faulty input, no name specified")
        res = (
            self.client()
                .post('/cupcakes',
                      json={'description': 'description of New Cupcake Faulty Name Missing',                            
                            'ingredients': [{'kind': 'topping', 'name': 'new topping for faulty cupcake'}]
                      })
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)


    # test deleting a cupcake, and check that it was really deleted
    def test_delete_cupcake(self):
        res = self.client().delete('/cupcakes/2')
        data = json.loads(res.data)

        cupcake = Cupcake.query.filter(Cupcake.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(cupcake, None)

    # test deleting a non-existent cupcake returns 404
    def test_delete_non_existent_cupcake(self):
        res = self.client().delete('/cupcakes/222')
        data = json.loads(res.data)


        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)


    # test updating a cupcake; changing its name and description
    def test_update_cupcake(self):
        res = self.client().patch('/cupcakes/3', 
                                  json = {"name": "change of name", "description": "new description", "ingredients": [] })

        data = json.loads(res.data)
        the_cupcake = (Cupcake.query
                              .filter(Cupcake.id==3)
                              .first()
        )
        self.assertEqual(the_cupcake.short()['name'], 'change of name')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # test updating a non-existent cupcake results in 404
    def test_update_non_existent_cupcake(self):
        res = self.client().patch('/cupcakes/300', 
                                  json = {"name": "change of name", "description": "new description", "ingredients": [] })

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)                                  

    # test getting orders
    def test_get_orders(self):
        print ("test GET orders")
        res = self.client().get('/orders')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['orders'])        
        self.assertEqual(data['success'], True)

    def test_get_specific_order(self):
        print ("test GET specific order")
        res = self.client().get('/orders/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['orders'])        
        self.assertEqual(data['success'], True)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()