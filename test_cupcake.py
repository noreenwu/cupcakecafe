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

    def test_get_cupcakes(self):
        res = self.client().get('/cupcakes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['cupcakes'])

    def test_get_specific_cupcake(self):
        res = self.client().get('/cupcakes/9')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['cupcakes'])

    def test_create_cupcake(self):
        res = (
            self.client()
                .post('/cupcakes',
                      json={'name': 'Chocolate Mocha Cream 119',
                            'description': 'intense combination of coffee and dark chocolate',
                            'ingredients': [{'kind': 'topping', 'name': 'chips'}]
                      })
        )
        data = json.loads(res.data)
        # verify that it was created in the database
        the_cupcake = (Cupcake.query
                              .filter_by(name='Chocolate Mocha Cream 119')  
                              .filter_by(description='intense combination of coffee and dark chocolate')
                              .first()
        )
        self.assertTrue(the_cupcake is not None)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_delete_cupcake(self):
        res = self.client().delete('/cupcakes/23')
        data = json.loads(res.data)

        cupcake = Cupcake.query.filter(Cupcake.id == 23).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(cupcake, None)


    def test_update_cupcake(self):
        res = self.client().patch('/cupcakes/9', 
                                  json = {"name": "HALLOW", "description": "new", "ingredients": [{"name": "carrot", "kind": "cake"}] })

        data = json.loads(res.data)
        the_cupcake = (Cupcake.query
                              .filter(Cupcake.id==9)
                              .first()
        )
        self.assertEqual(the_cupcake.short()['name'], 'HALLOW')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()