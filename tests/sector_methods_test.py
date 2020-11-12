import unittest

from __init__ import create_app
from database.database import db


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

    def test_add_sector(self):

        url = f'{BASE_URL}/add/{self.sector["name"]}'

        # Add
        response = self.client().post(url, json=self.sector)

        # Verify
        response_code = response.status_code
        expected_code = 200
        self.assertEqual(expected_code, response_code)

        response_json_str = str(response.get_json())
        self.assertIn('Tecnologia', response_json_str)

    def test_add_sector_with_empty_parameters(self):

        sector = {}
        url = f'{BASE_URL}/add/test'

        # Add
        response = self.client().post(url, json=sector)

        # Verify
        response_code = response.status_code
        expected_code = 422
        self.assertEqual(expected_code, response_code)

        response_json_str = str(response.get_json())
        self.assertIn('Missing data for required field', response_json_str)

    def test_add_sector_given_invalid_parameters(self):

        sector = {'name': 123}
        url = f'{BASE_URL}/add/test'

        # Add
        response = self.client().post(url, json=sector)

        # Verify
        response_code = response.status_code
        expected_code = 422
        self.assertEqual(expected_code, response_code)

        response_json_str = str(response.get_json())
        self.assertIn('Not a valid', response_json_str)

    def test_add_sector_that_already_exists(self):

        url = f'{BASE_URL}/add/{self.sector["name"]}'

        # Add the sector once
        self.client().post(url, json=self.sector)

        # Try to add the same sector again
        response = self.client().post(url, json=self.sector)

        # Verify
        response_code = response.status_code
        expected_code = 409
        self.assertEqual(expected_code, response_code)

        response_json_str = str(response.get_json())
        self.assertIn(f'Sector already exists with name = {self.sector["name"]}', response_json_str)

    def test_list_all_sectors(self):

        # Add sectors
        sector1 = {'name': 'Recursos Humanos'}
        sector2 = {'name': 'Recursos Tecnológicos'}
        sector3 = {'name': 'Limpeza'}
        sectors = [sector1, sector2, sector3]
        for sector in sectors:
            self.client().post(f'{BASE_URL}/add/{sector["name"]}', json=sector)

        # Retrieve the data
        url = f'{BASE_URL}/all'
        response = self.client().get(url)

        # Verify
        response_code = response.status_code
        expected_code = 200
        self.assertEqual(expected_code, response_code)

        response_json_str = str(response.get_json())
        self.assertIn('Recursos Humanos', response_json_str)
        self.assertIn('Recursos Tecnológicos', response_json_str)
        self.assertIn('Limpeza', response_json_str)

    def test_list_all_sectors_empty(self):

        # Retrieve the data
        url = f'{BASE_URL}/all'
        response = self.client().get(url)

        # Verify
        response_code = response.status_code
        expected_code = 404
        self.assertEqual(expected_code, response_code)

        response_json_str = str(response.get_json())
        self.assertIn('No sectors found', response_json_str)

    def test_list_all_sectors_filtered_by_name(self):

        # Insert sectors
        sector1 = {'name': 'Recursos Humanos'}
        sector2 = {'name': 'Recursos Tecnológicos'}
        sector3 = {'name': 'Limpeza'}
        sectors = [sector1, sector2, sector3]

        for sector in sectors:
            self.client().post(f'{BASE_URL}/add/{sector["name"]}', json=sector)

        # Try to retrieve the sectors filtered by name
        url = BASE_URL + '/all/Recursos'
        response = self.client().get(url)

        # Verify
        response_code = response.status_code
        expected_code = 200
        self.assertEqual(response_code, expected_code)

        response_json_str = str(response.get_json())
        self.assertIn('Humanos', response_json_str)
        self.assertIn('Tecnológicos', response_json_str)
        self.assertNotIn('Limpeza', response_json_str)

    def test_get_sector_by_name(self):

        # Insert sectors
        sector1 = {'name': 'Recursos Humanos'}
        sector2 = {'name': 'Recursos Tecnológicos'}
        sector3 = {'name': 'Limpeza'}
        sectors = [sector1, sector2, sector3]

        for sector in sectors:
            self.client().post(f'{BASE_URL}/add/{sector["name"]}', json=sector)

        # Try to retrieve each sector by name
        for sector in sectors:
            sector_name = sector['name']
            url = f'{BASE_URL}/{sector_name}'

            # Verify
            response = self.client().get(url)
            response_code = response.status_code
            expected_code = 200
            self.assertEqual(response_code, expected_code)

            response_json_str = str(response.get_json())
            self.assertIn(sector_name, response_json_str)
            self.assertIn(sector_name, response_json_str)
            self.assertIn(sector_name, response_json_str)

    def test_get_sector_that_does_not_exist(self):

        url = BASE_URL + f'/add/{self.sector["name"]}'

        # Add the sector
        self.client().post(url, json=self.sector)

        # Try to retrieve a sector that does not exist
        sector = {'name': 'Negócios'}
        url = f'{BASE_URL}/{sector["name"]}'

        # Verify
        response = self.client().get(url)
        response_code = response.status_code
        expected_code = 404
        self.assertEqual(response_code, expected_code)

        response_json_str = str(response.get_json())
        self.assertIn(f'Sector not found with name = {sector["name"]}', response_json_str)

    def test_update_sector(self):

        sector_name = self.sector['name']

        # Insert the sector
        self.client().post(f'{BASE_URL}/add/{sector_name}', json=self.sector)

        # Try to update it
        temp = self.sector.copy()
        temp['name'] = 'Segurança da Informação'

        url = f'{BASE_URL}/update/{sector_name}'
        response = self.client().put(url, json=temp)

        # Verify
        response_code = response.status_code
        expected_code = 200
        self.assertEqual(response_code, expected_code)

        response_json_str = str(response.get_json())
        self.assertIn('Segurança da Informação', response_json_str)

        # Check whether the update took effect
        url = f'{BASE_URL}/{sector_name}'

        response = self.client().get(url)
        response_code = response.status_code
        expected_code = 404
        self.assertEqual(response_code, expected_code)

        response_json_str = str(response.get_json())
        self.assertEqual(f"{{'Error': 'Sector not found with name = {sector_name}'}}", response_json_str)

    def test_update_sector_given_empty_parameters(self):

        # Insert the sector
        sector_name = self.sector['name']
        self.client().post(f'{BASE_URL}/add/{sector_name}', json=self.sector)

        # Try to update it with an empty sector
        empty_sector = {}

        url = f'{BASE_URL}/update/{self.sector["name"]}'
        response = self.client().put(url, json=empty_sector)

        # Verify
        response_code = response.status_code
        expected_code = 422
        self.assertEqual(expected_code, response_code)

        response_json_str = str(response.get_json())
        self.assertIn('Missing data for required field', response_json_str)

    def test_update_sector_given_invalid_parameters(self):

        # Insert the sector
        sector_name = self.sector['name']
        self.client().post(f'{BASE_URL}/add/{sector_name}', json=self.sector)

        # Try to update it with an invalid parameter
        new_sector = {'name': 123}
        url = f'{BASE_URL}/update/{self.sector["name"]}'
        response = self.client().put(url, json=new_sector)

        # Verify
        response_code = response.status_code
        expected_code = 422
        self.assertEqual(expected_code, response_code)

        response_json_str = str(response.get_json())
        self.assertIn('Not a valid', response_json_str)

    def test_update_sector_that_doesnt_exist(self):

        # Try to update a sector that doesn't exist
        sector = {'name': 'Does not exist'}
        url = BASE_URL + f'/update/{sector["name"]}'
        response = self.client().put(url, json=sector)

        # Verify
        response_code = response.status_code
        expected_code = 404
        self.assertEqual(expected_code, response_code)

        response_json_str = str(response.get_json())
        self.assertIn(f'Sector not found with name = {sector["name"]}', response_json_str)

    def test_delete_sector(self):

        # Insert the sector
        sector_name = self.sector["name"]
        self.client().post(f'{BASE_URL}/add/{sector_name}', json=self.sector)

        # Try to delete it
        url = f'{BASE_URL}/delete/{sector_name}'
        response = self.client().delete(url)

        # Verify
        response_code = response.status_code
        expected_code = 200
        self.assertEqual(response_code, expected_code)

        response_json_str = str(response.get_json())
        self.assertIn('Successfully deleted', response_json_str)

        # Check whether the deletion took effect
        url = f'{BASE_URL}/{sector_name}'
        response = self.client().get(url)

        # Verify
        response_code = response.status_code
        expected_code = 404
        self.assertEqual(response_code, expected_code)

        response_json_str = str(response.get_json())
        self.assertEqual(f"{{'Error': 'Sector not found with name = {sector_name}'}}", response_json_str)

    def test_delete_sector_that_doesnt_exist(self):

        # Try to delete the sector that is not in the database
        url = f'{BASE_URL}/delete/{self.sector["name"]}'
        response = self.client().delete(url)

        # Verify
        response_code = response.status_code
        expected_code = 404
        self.assertEqual(response_code, expected_code)

        response_json_str = str(response.get_json())
        self.assertIn(f'Sector not found with name = {self.sector["name"]}', response_json_str)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == '__main__':
    unittest.main()
