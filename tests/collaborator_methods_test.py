import unittest


from __init__ import create_app
from core.database import db
from datetime import datetime


COLLABORATORS_BASE_URL = 'http://127.0.0.1:5000/collaborators'
SECTORS_BASE_URL = 'http://127.0.0.1:5000/sectors'



class CollaboratorTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client

        today = datetime(year=2020, month=11, day=11)

        self.collaborator = {
            'collab_number': 12345,
            'full_name': 'Bernardino',
            'birth_date': str(today),
            'current_salary': 123.45,
            'active': True,
            'sector_name': 'Tecnologia'
        }

        self.sector = {'name': 'Tecnologia'}

        with self.app.app_context():
            db.create_all()

    def test_collaborator_add(self):
        """ Test if the API can create a collaborator (POST request) """

        # First, we add a sector (because it is required in order to add a collaborator)
        self.client().post(f'{SECTORS_BASE_URL}/add/{self.sector["name"]}', json=self.sector)

        # Then, we try to add a new collaborator in that sector
        url = COLLABORATORS_BASE_URL + f'/add/{self.collaborator["collab_number"]}'
        response = self.client().post(url, json=self.collaborator)

        response_code = response.status_code
        expected_code = 200

        response_json_str = str(response.get_json())

        self.assertEqual(expected_code, response_code)
        self.assertIn(str(self.collaborator['collab_number']), response_json_str)

    def test_collaborator_add_no_parameters(self):
        """ Test if the API can create an empty collaborator (POST request) """

        # First, we add a sector (because it is required in order to add a collaborator)
        self.client().post(f'{SECTORS_BASE_URL}/add/{self.sector["name"]}', json=self.sector)

        # Then, we try to add an empty collaborator
        url = COLLABORATORS_BASE_URL + f'/add/{self.collaborator["collab_number"]}'
        empty_collaborator = {}
        response = self.client().post(url, json=empty_collaborator)

        response_code = response.status_code
        expected_code = 422

        response_json_str = str(response.get_json())

        self.assertEqual(expected_code, response_code)
        self.assertIn('parameters are required', response_json_str)

    def test_collaborator_add_invalid_parameter_types(self):
        """ Test if the API can create a collaborator with invalid parameter types (POST request) """

        # First, we add a sector (because it is required in order to add a collaborator)
        self.client().post(f'{SECTORS_BASE_URL}/add/{self.sector["name"]}', json=self.sector)

        # Then, we try to add a collaborator with invalid parameters
        url = COLLABORATORS_BASE_URL + f'/add/{self.collaborator["collab_number"]}'

        invalid_collaborator = {
            'collab_number': 'TESTE',
            'full_name': 1234,
            'birth_date': 3.14,
            'current_salary': 'Joao',
            'active': -2,
            'sector_name': True
        }

        response = self.client().post(url, json=invalid_collaborator)

        response_code = response.status_code
        expected_code = 422

        response_json_str = str(response.get_json())

        self.assertEqual(expected_code, response_code)
        self.assertIn('Wrong parameter type', response_json_str)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
