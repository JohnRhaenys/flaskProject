import unittest

from __init__ import create_app
from core.database import db


BASE_URL = 'http://127.0.0.1:5000/sectors'


class SectorTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client

        self.sector = {
            'name': 'Tecnologia'
        }

        with self.app.app_context():
            db.create_all()

    def test_sector_add(self):
        """ Test if the API can create a sector (POST request) """
        url = BASE_URL + f'/add/{self.sector["name"]}'

        response = self.client().post(url, json=self.sector)

        response_code = response.status_code
        expected_code = 200

        response_json_str = str(response.get_json())

        self.assertEqual(expected_code, response_code)
        self.assertIn('Tecnologia', response_json_str)

    def test_sector_add_no_parameters(self):
        """ Test if the API can create a sector with missing parameters (POST request) """
        sector = {}
        url = BASE_URL + f'/add/test'

        response = self.client().post(url, json=sector)

        response_code = response.status_code
        expected_code = 422

        response_json_str = str(response.get_json())

        self.assertEqual(expected_code, response_code)
        self.assertIn('parameters are required', response_json_str)

    def test_sector_add_invalid_parameter_type(self):
        """ Test if the API can create a sector with invalid parameter types (POST request) """
        sector = {'name': 123}
        url = BASE_URL + f'/add/test'

        response = self.client().post(url, json=sector)

        response_code = response.status_code
        expected_code = 422

        response_json_str = str(response.get_json())

        self.assertEqual(expected_code, response_code)
        self.assertIn('Wrong parameter type', response_json_str)

    def test_list_all_sectors(self):
        """ Test if the API can list all sectors (GET request) """

        # Insert sectors
        sector1 = {'name': 'Recursos Humanos'}
        sector2 = {'name': 'Recursos Tecnológicos'}
        sector3 = {'name': 'Limpeza'}
        sectors = [sector1, sector2, sector3]
        for sector in sectors:
            response = self.client().post(f'{BASE_URL}/add/{sector["name"]}', json=sector)
            response_code = response.status_code
            expected_code = 200
            self.assertEqual(response_code, expected_code)

        # Retrieve the data
        url = BASE_URL + '/all'
        response = self.client().get(url)
        response_code = response.status_code
        expected_code = 200
        response_json_str = str(response.get_json())

        # Verify the response
        self.assertEqual(expected_code, response_code)
        self.assertIn('Recursos Humanos', response_json_str)
        self.assertIn('Recursos Tecnológicos', response_json_str)
        self.assertIn('Limpeza', response_json_str)

    def test_list_all_sectors_filtered(self):
        """ Test if the API can list all sectors filtered by name (GET request) """

        sector1 = {'name': 'Recursos Humanos'}
        sector2 = {'name': 'Recursos Tecnológicos'}
        sector3 = {'name': 'Limpeza'}
        sectors = [sector1, sector2, sector3]

        # Insert sectors
        for sector in sectors:
            response = self.client().post(f'{BASE_URL}/add/{sector["name"]}', json=sector)
            response_code = response.status_code
            expected_code = 200
            self.assertEqual(response_code, expected_code)

        # Try to retrieve the sectors filtered by name
        url = BASE_URL + '/all/Recursos'
        response = self.client().get(url)

        # Verify response code
        response_code = response.status_code
        expected_code = 200
        self.assertEqual(response_code, expected_code)

        # Verify response content
        response_json_str = str(response.get_json())
        self.assertIn('Humanos', response_json_str)
        self.assertIn('Tecnológicos', response_json_str)
        self.assertNotIn('Limpeza', response_json_str)

    def test_api_can_get_sector_by_name(self):
        """ Test if the API can get a single sector by using its id (GET request) """

        sector1 = {'name': 'Recursos Humanos'}
        sector2 = {'name': 'Recursos Tecnológicos'}
        sector3 = {'name': 'Limpeza'}
        sectors = [sector1, sector2, sector3]

        # Insert sectors
        for sector in sectors:
            response = self.client().post(f'{BASE_URL}/add/{sector["name"]}', json=sector)
            response_code = response.status_code
            expected_code = 200
            self.assertEqual(response_code, expected_code)

        # Try to retrieve each sector by name
        for sector in sectors:
            sector_name = sector['name']
            url = BASE_URL + f'/{sector_name}'

            # Verify response code
            response = self.client().get(url)
            response_code = response.status_code
            expected_code = 200
            self.assertEqual(response_code, expected_code)

            # Verify response content
            response_json_str = str(response.get_json())
            self.assertIn(sector_name, response_json_str)
            self.assertIn(sector_name, response_json_str)
            self.assertIn(sector_name, response_json_str)

    def test_api_can_update_sector(self):
        """ Test if the API can update a single sector by using its name (PUT) """
        sector_name = self.sector['name']

        # Insert the sector
        response = self.client().post(f'{BASE_URL}/add/{sector_name}', json=self.sector)
        response_code = response.status_code
        expected_code = 200
        self.assertEqual(response_code, expected_code)

        # Try to update it
        temp = self.sector.copy()
        temp['name'] = 'Segurança da Informação'

        url = BASE_URL + f'/update/{sector_name}'
        response = self.client().put(url, json=temp)

        # Verify the response code
        response_code = response.status_code
        expected_code = 200
        self.assertEqual(response_code, expected_code)

        # Verify response content
        response_json_str = str(response.get_json())
        self.assertIn('Segurança da Informação', response_json_str)

        # Check whether the update took effect
        url = BASE_URL + f'/{sector_name}'

        response = self.client().get(url)
        response_code = response.status_code
        expected_code = 404
        self.assertEqual(response_code, expected_code)

        response_json_str = str(response.get_json())
        self.assertEqual(f"{{'Error': 'Sector not found with name = {sector_name}'}}", response_json_str)

    def test_api_can_delete_sector(self):
        """ Test if the API can delete a single sector by using its name (DELETE) """

        # Insert the sector
        sector_name = self.sector["name"]

        response = self.client().post(f'{BASE_URL}/add/{sector_name}', json=self.sector)
        response_code = response.status_code
        expected_code = 200
        self.assertEqual(response_code, expected_code)

        # Try to delete it
        url = f'{BASE_URL}/delete/{sector_name}'
        response = self.client().delete(url)

        # Verify the response code
        response_code = response.status_code
        expected_code = 200
        self.assertEqual(response_code, expected_code)

        # Verify response content
        response_json_str = str(response.get_json())
        self.assertIn('Successfully deleted', response_json_str)

        # Check whether the deletion took effect
        url = BASE_URL + f'/{sector_name}'

        response = self.client().get(url)
        response_code = response.status_code
        expected_code = 404
        self.assertEqual(response_code, expected_code)

        response_json_str = str(response.get_json())
        self.assertEqual(f"{{'Error': 'Sector not found with name = {sector_name}'}}", response_json_str)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
