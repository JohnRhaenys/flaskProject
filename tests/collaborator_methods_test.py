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

    def test_add_collaborator(self):
        """ Test if the API can add a collaborator (POST request) """

        # Add a sector (because it is required in order to add a collaborator)
        # Fix this later using DEPENDENCY INJECTION
        self.client().post(f'{SECTORS_BASE_URL}/add/{self.sector["name"]}', json=self.sector)

        collab_number = self.collaborator["collab_number"]

        # Try to add a new collaborator
        url = f'{COLLABORATORS_BASE_URL}/add/{collab_number}'
        response = self.client().post(url, json=self.collaborator)

        # Verify the response code
        response_code = response.status_code
        expected_code = 200
        self.assertEqual(expected_code, response_code)

        # Verify the response content
        response_json_str = str(response.get_json())
        self.assertIn(str(collab_number), response_json_str)

    def test_add_collaborator_with_no_parameters(self):
        """ Test if the API can create a collaborator given no parameters - (POST request) """

        # Add a sector
        self.client().post(f'{SECTORS_BASE_URL}/add/{self.sector["name"]}', json=self.sector)

        collab_number = self.collaborator["collab_number"]

        # Try to add an empty collaborator
        url = COLLABORATORS_BASE_URL + f'/add/{collab_number}'
        empty_collaborator = {}
        response = self.client().post(url, json=empty_collaborator)

        # Verify the response code
        response_code = response.status_code
        expected_code = 422
        self.assertEqual(expected_code, response_code)

        # Verify the response content
        response_json_str = str(response.get_json())
        self.assertIn('parameters are required', response_json_str)

    def test_add_collaborator_with_invalid_parameter_types(self):
        """ Test if the API can create a collaborator with invalid parameter types - (POST request) """

        # Add a sector
        self.client().post(f'{SECTORS_BASE_URL}/add/{self.sector["name"]}', json=self.sector)

        collab_number = self.collaborator['collab_number']

        # Try to add a collaborator with invalid parameters
        url = COLLABORATORS_BASE_URL + f'/add/{collab_number}'

        invalid_collaborator = {
            'collab_number': 'TESTE',
            'full_name': 1234,
            'birth_date': 3.14,
            'current_salary': 'Joao',
            'active': -2,
            'sector_name': True
        }

        response = self.client().post(url, json=invalid_collaborator)

        # Verify the response code
        response_code = response.status_code
        expected_code = 422
        self.assertEqual(expected_code, response_code)

        # Verify the response content
        response_json_str = str(response.get_json())
        self.assertIn('Wrong parameter type', response_json_str)

    def test_add_collaborator_already_exists(self):
        """ Test if the API can add a collaborator that already exists - (POST request) """

        # Add a sector
        self.client().post(f'{SECTORS_BASE_URL}/add/{self.sector["name"]}', json=self.sector)

        collab_number = self.collaborator['collab_number']

        # Add a new collaborator
        url = COLLABORATORS_BASE_URL + f'/add/{collab_number}'
        self.client().post(url, json=self.collaborator)

        # Try to add the same collaborator again
        response = self.client().post(url, json=self.collaborator)

        # Verify the response code
        response_code = response.status_code
        expected_code = 409
        self.assertEqual(expected_code, response_code)

        # Verify the response content
        response_json_str = str(response.get_json())
        self.assertIn(f'Collaborator already exists with number = {collab_number}', response_json_str)

    def test_list_all_collaborators(self):

        self.client().post(f'{SECTORS_BASE_URL}/add/{self.sector["name"]}', json=self.sector)

        # Insert collaborators
        collaborator2 = self.collaborator.copy()
        collaborator2['collab_number'] = 10
        collaborator2['full_name'] = 'Joao'

        collaborator3 = self.collaborator.copy()
        collaborator3['collab_number'] = 20
        collaborator3['full_name'] = 'Anna'

        collaborators = [self.collaborator, collaborator2, collaborator3]
        for collaborator in collaborators:
            self.client().post(
                f'{COLLABORATORS_BASE_URL}/add/{collaborator["collab_number"]}', json=collaborator
            )

        # Retrieve the data
        url = f'{COLLABORATORS_BASE_URL}/all'
        response = self.client().get(url)

        # Verify the response code
        response_code = response.status_code
        expected_code = 200

        # Verify the response content
        response_json_str = str(response.get_json())
        self.assertEqual(expected_code, response_code)
        self.assertIn('Bernardino', response_json_str)
        self.assertIn('Joao', response_json_str)
        self.assertIn('Anna', response_json_str)

    def test_list_all_collaborators_filtered_by_name(self):

        self.client().post(f'{SECTORS_BASE_URL}/add/{self.sector["name"]}', json=self.sector)

        # Insert collaborators
        collaborator2 = self.collaborator.copy()
        collaborator2['collab_number'] = 10
        collaborator2['full_name'] = 'Joao Vitor Andrade'

        collaborator3 = self.collaborator.copy()
        collaborator3['collab_number'] = 20
        collaborator3['full_name'] = 'Joao Pedro Da Silva'

        collaborators = [self.collaborator, collaborator2, collaborator3]
        for collaborator in collaborators:
            self.client().post(
                f'{COLLABORATORS_BASE_URL}/add/{collaborator["collab_number"]}', json=collaborator
            )

        # Retrieve the data
        url = f'{COLLABORATORS_BASE_URL}/all/Joao'
        response = self.client().get(url)

        # Verify the response code
        response_code = response.status_code
        expected_code = 200
        response_json_str = str(response.get_json())

        # Verify the response content
        self.assertEqual(expected_code, response_code)
        self.assertIn('Joao Vitor', response_json_str)
        self.assertIn('Joao Pedro', response_json_str)
        self.assertNotIn('Bernardino', response_json_str)

    def test_list_all_collaborators_empty(self):

        # Retrieve the data
        url = f'{COLLABORATORS_BASE_URL}/all'
        response = self.client().get(url)

        # Verify the response code
        response_code = response.status_code
        expected_code = 404
        response_json_str = str(response.get_json())
        self.assertEqual(expected_code, response_code)

        # Verify the response content
        self.assertIn('No collaborators found', response_json_str)

    def test_get_collaborator_by_number(self):

        self.client().post(f'{SECTORS_BASE_URL}/add/{self.sector["name"]}', json=self.sector)

        # Insert collaborators
        collaborator2 = self.collaborator.copy()
        collaborator2['collab_number'] = 10
        collaborator2['full_name'] = 'Joao Vitor Andrade'

        collaborator3 = self.collaborator.copy()
        collaborator3['collab_number'] = 20
        collaborator3['full_name'] = 'Joao Pedro Da Silva'

        collaborators = [self.collaborator, collaborator2, collaborator3]
        for collaborator in collaborators:
            self.client().post(
                f'{COLLABORATORS_BASE_URL}/add/{collaborator["collab_number"]}', json=collaborator
            )

        # Try to retrieve each sector by name
        for collaborator in collaborators:
            collab_number = collaborator['collab_number']
            url = f'{COLLABORATORS_BASE_URL}/{collab_number}'

            # Verify response code
            response = self.client().get(url)
            response_code = response.status_code
            expected_code = 200
            self.assertEqual(response_code, expected_code)

            # Verify response content
            response_json_str = str(response.get_json())
            self.assertIn(str(collaborator['collab_number']), response_json_str)

    def test_get_collaborator_that_doesnt_exist(self):

        self.client().post(f'{SECTORS_BASE_URL}/add/{self.sector["name"]}', json=self.sector)

        # Add a collaborator
        url = COLLABORATORS_BASE_URL + f'/add/{self.collaborator["collab_number"]}'
        self.client().post(url, json=self.collaborator)

        # Try to retrieve a collaborator who does not exist
        url = f'{COLLABORATORS_BASE_URL}/-200'
        response = self.client().get(url)

        # Verify response code
        response_code = response.status_code
        expected_code = 404
        self.assertEqual(response_code, expected_code)

        # Verify response content
        response_json_str = str(response.get_json())
        self.assertIn('Collaborator not found with number = -200', response_json_str)

    def test_get_collaborator_by_number_given_invalid_parameters(self):

        self.client().post(f'{SECTORS_BASE_URL}/add/{self.sector["name"]}', json=self.sector)

        # Add a collaborator
        url = COLLABORATORS_BASE_URL + f'/add/{self.collaborator["collab_number"]}'
        self.client().post(url, json=self.collaborator)

        # Try to get a collaborator using an invalid parameter type
        invalid_number = 'STRING_TEST'
        url = f'{COLLABORATORS_BASE_URL}/{invalid_number}'
        response = self.client().get(url)

        # Verify response code
        response_code = response.status_code
        expected_code = 400
        self.assertEqual(response_code, expected_code)

        # Verify response content
        response_json_str = str(response.get_json())
        self.assertIn(f"The parameter '{invalid_number}' cannot be parsed", response_json_str)

    def test_update_collaborator(self):

        self.client().post(f'{SECTORS_BASE_URL}/add/{self.sector["name"]}', json=self.sector)

        # Add a collaborator
        url = COLLABORATORS_BASE_URL + f'/add/{self.collaborator["collab_number"]}'
        self.client().post(url, json=self.collaborator)

        # Change a field in the collaborator
        updated_data = self.collaborator.copy()
        updated_data['current_salary'] = 9999.00

        # Try to update the collaborator
        url = f'{COLLABORATORS_BASE_URL}/update/{updated_data["collab_number"]}'
        response = self.client().put(url, json=updated_data)

        # Verify response code
        response_code = response.status_code
        expected_code = 200
        self.assertEqual(response_code, expected_code)

        # Verify response content
        response_json_str = str(response.get_json())
        self.assertEqual(str(updated_data), response_json_str)

    def test_update_collaborator_given_empty_parameters(self):

        self.client().post(f'{SECTORS_BASE_URL}/add/{self.sector["name"]}', json=self.sector)

        collab_number = self.collaborator["collab_number"]

        # Add a collaborator
        url = f'{COLLABORATORS_BASE_URL}/add/{collab_number}'
        self.client().post(url, json=self.collaborator)

        # Try to update the collaborator passing an empty object_model
        url = f'{COLLABORATORS_BASE_URL}/update/{collab_number}'
        empty_data = {}
        response = self.client().put(url, json=empty_data)

        # Verify response code
        response_code = response.status_code
        expected_code = 422
        self.assertEqual(response_code, expected_code)

        # Verify response content
        response_json_str = str(response.get_json())
        self.assertIn('parameters are required', response_json_str)

    def test_update_collaborator_given_invalid_parameters(self):

        self.client().post(f'{SECTORS_BASE_URL}/add/{self.sector["name"]}', json=self.sector)

        collab_number = self.collaborator['collab_number']

        # Add a collaborator
        url = f'{COLLABORATORS_BASE_URL}/add/{collab_number}'
        self.client().post(url, json=self.collaborator)

        # Try to update the collaborator passing invalid parameters
        url = COLLABORATORS_BASE_URL + f'/update/{collab_number}'

        invalid_collaborator = {
            'collab_number': self.collaborator['collab_number'],
            'full_name': 1234,
            'birth_date': 3.14,
            'current_salary': 'Teste',
            'active': -2,
            'sector_name': True
        }

        response = self.client().put(url, json=invalid_collaborator)

        # Verify response code
        response_code = response.status_code
        expected_code = 422
        self.assertEqual(response_code, expected_code)

        # Verify response content
        response_json_str = str(response.get_json())
        self.assertIn('Wrong parameter type', response_json_str)

    def test_update_collaborator_that_doesnt_exist(self):

        collab_number = self.collaborator['collab_number']

        # Try to update a collaborator that doesn't exist
        url = COLLABORATORS_BASE_URL + f'/update/{collab_number}'

        response = self.client().put(url, json=self.collaborator)

        # Verify response code
        response_code = response.status_code
        expected_code = 404
        self.assertEqual(response_code, expected_code)

        # Verify response content
        response_json_str = str(response.get_json())
        self.assertEqual(
            f"{{'Error': 'Collaborator not found with number = {collab_number}'}}", response_json_str
        )

    def test_delete_collaborator(self):

        self.client().post(f'{SECTORS_BASE_URL}/add/{self.sector["name"]}', json=self.sector)

        collaborator_number = self.collaborator['collab_number']

        # Add a collaborator
        url = f'{COLLABORATORS_BASE_URL}/add/{collaborator_number}'
        self.client().post(url, json=self.collaborator)

        # Try to remove the collaborator
        url = f'{COLLABORATORS_BASE_URL}/delete/{collaborator_number}'
        response = self.client().delete(url)

        # Verify response code
        response_code = response.status_code
        expected_code = 200
        self.assertEqual(response_code, expected_code)

        # Verify response content
        response_json_str = str(response.get_json())
        self.assertIn('Successfully deleted', response_json_str)

        # Check whether the deletion took effect
        url = f'{COLLABORATORS_BASE_URL}/{collaborator_number}'
        response = self.client().get(url)

        # Verify response code
        response_code = response.status_code
        expected_code = 404
        self.assertEqual(response_code, expected_code)

        # Verify response content
        response_json_str = str(response.get_json())
        self.assertEqual(
            f"{{'Error': 'Collaborator not found with number = {collaborator_number}'}}", response_json_str
        )

    def test_delete_collaborator_given_invalid_parameters(self):

        self.client().post(f'{SECTORS_BASE_URL}/add/{self.sector["name"]}', json=self.sector)

        collaborator_number = self.collaborator['collab_number']

        # Add a collaborator
        url = COLLABORATORS_BASE_URL + f'/add/{collaborator_number}'
        self.client().post(url, json=self.collaborator)

        # Try to remove the collaborator
        invalid_number = 'NUMBER_TEST'
        url = f'{COLLABORATORS_BASE_URL}/delete/{invalid_number}'
        response = self.client().delete(url)

        # Verify response code
        response_code = response.status_code
        expected_code = 400
        self.assertEqual(response_code, expected_code)

        # Verify response content
        response_json_str = str(response.get_json())
        self.assertIn('cannot be parsed', response_json_str)

    def test_delete_collaborator_that_doesnt_exist(self):

        self.client().post(f'{SECTORS_BASE_URL}/add/{self.sector["name"]}', json=self.sector)

        collaborator_number = self.collaborator['collab_number']

        # Add a collaborator
        url = f'{COLLABORATORS_BASE_URL}/add/{collaborator_number}'
        self.client().post(url, json=self.collaborator)

        # Try to remove the collaborator
        not_in_database = -100
        url = f'{COLLABORATORS_BASE_URL}/delete/{not_in_database}'
        response = self.client().delete(url)

        # Verify response code
        response_code = response.status_code
        expected_code = 404
        self.assertEqual(response_code, expected_code)

        # Verify response content
        response_json_str = str(response.get_json())
        self.assertIn(f'Collaborator not found with number = {not_in_database}', response_json_str)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
