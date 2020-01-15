import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy


from app import create_app
from models import setup_db, Cupcake, Ingredient


class Cupcake(unittest.TestCase):
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

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()