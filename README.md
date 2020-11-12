# flaskProject

REST API for manipulating data about sectors and collaborators in a company.

Language and technologies: Python (Version 3.6.9), Flask, SQLAlchemy and Marshmallow.

Functionalities:
1) The API offers endpoints for listing, reading, creating, updating and deleting sectors and collaborators.
2) It is possible to list objects in a range (using the object ID) or by name (using a filter).

Setup: 
In order to properly setup the project, please install the required dependencies listed in the "requirements.txt" file.

Extras:
A "tests" folder is included in the project. In order to automatically evaluate the functionalities, please run the files "collaborator_methods_test.py" and "sector_methods_test.py" inside the "tests" folder.


Run:
To run the API, please execute the "run.py" file. The API will be executed locally (localhost http://127.0.0.1:5000)


EXAMPLES (THE SAME USAGE APPLIES TO THE SECTORS):

**ADD A COLLABORATOR**
```python
from datetime import datetime
today = datetime(year=2020, month=11, day=12)
collaborator = {
    'collab_number': 1,
    'full_name': 'Bernardino',
    'birth_date': str(today),
    'current_salary': 123.45,
    'active': True,
    'sector_name': 'Tecnologia'
}

# Url = 'http://127.0.0.1:5000/collaborators/add/1
response = requests.post(f'{COLLABORATORS_URL}/add/{collaborator["collab_number"]}', json=collaborator)
print('Response code: ', response.status_code)
print('Response JSON: ', response.json())
```

OUTPUT:    
Response code: 200  
Response JSON: {'collab_number': 1, 'full_name': 'Bernardino', 'birth_date': '2020-11-12 00:00:00', 'current_salary': 123.45, 'active': True, 'sector_name': 'Tecnologia'}  


**LIST ALL COLLABORATORS:**

```python
BASE_URL = 'http://127.0.0.1:5000'
COLLABORATORS_URL = f'{BASE_URL}/collaborators'

# List all collaborators, ordered by name
# Url = 'http://127.0.0.1:5000/collaborators/all
response = requests.get(f'{COLLABORATORS_URL}/all')
print('Response code: ', response.status_code)
print('Response JSON: ', response.json())
```

OUTPUT:  
Response code:  200  
Response JSON:  [{'collab_number': 1, 'full_name': 'Bernardino', 'birth_date': '2020-11-12 00:00:00', 'current_salary': 123.45, 'active': True}, {'collab_number': 3, 'full_name': 'Joao Pedro', 'birth_date': '2020-11-12 00:00:00', 'current_salary': 6.28, 'active': True}, {'collab_number': 2, 'full_name': 'Joao Vitor', 'birth_date': '2020-11-12 00:00:00', 'current_salary': 3.14, 'active': True}]  


**LIST ALL COLLABORATORS IN A RANGE:**
```python
# List all collaborators in a range of values 
# In this case, the API will return a JSON containing all collaborators with id between 0 and 10 (inclusively)
lower_bound = 0
upper_bound = 10

# Url = 'http://127.0.0.1:5000/collaborators/all/0/10
response = requests.get(f'{COLLABORATORS_URL}/all/{lower_bound}/{upper_bound}')
print('Response code: ', response.status_code)
print('Response JSON: ', response.json())
```
OUTPUT:  
Response code:  200    
Response JSON:  [{'collab_number': 1, 'full_name': 'Bernardino', 'birth_date': '2020-11-12 00:00:00', 'current_salary': 123.45, 'active': True}, {'collab_number': 2, 'full_name': 'Joao Vitor', 'birth_date': '2020-11-12 00:00:00', 'current_salary': 3.14, 'active': True}, {'collab_number': 3, 'full_name': 'Joao Pedro', 'birth_date': '2020-11-12 00:00:00', 'current_salary': 6.28, 'active': True}]    

**LIST ALL COLLABORATORS FILTERED BY NAME**
```python
# List all collaborators filtered by name
# In this case, the API will return a JSON containing all collaborators whose names match the filter (using the LIKE operator in the query)
# So, if there are collaborators with the names 'Joao Vitor' and 'Joao Pedro', and the name filter is 'Joao', then both collaborators will be returned
name_filter = 'Joao'
response = requests.get(f'{COLLABORATORS_URL}/all/{name_filter}')
print('Response code: ', response.status_code)
print('Response JSON: ', response.json())
```

OUTPUT:    
Response code:  200  
Response JSON:  [{'collab_number': 3, 'full_name': 'Joao Pedro', 'birth_date': '2020-11-12 00:00:00', 'current_salary': 6.28, 'active': True}, {'collab_number': 2, 'full_name': 'Joao Vitor', 'birth_date': '2020-11-12 00:00:00', 'current_salary': 3.14, 'active': True}]  


**GET A COLLABORATOR**
```python
# Get a single collaborator
collab_number = 1
response = requests.get(f'{COLLABORATORS_URL}/{collab_number}')
print('Response code: ', response.status_code)
print('Response JSON: ', response.json())
```

OUTPUT:    
Response code:  200  
Response JSON:  {'collab_number': 1, 'full_name': 'Bernardino', 'birth_date': '2020-11-12 00:00:00', 'current_salary': 123.45, 'active': True}  


**UPDATE A COLLABORATOR**
```python
# For instance, update the salary of a collaborator
updated_collaborator = {
    'collab_number': 1,
    'full_name': 'Bernardino',
    'birth_date': str(today),
    'current_salary': 999.99,
    'active': True,
    'sector_name': 'Tecnologia'
}
response = requests.put(f'{COLLABORATORS_URL}/update/1', json=updated_collaborator)
print('Response code: ', response.status_code)
print('Response JSON: ', response.json())
```
OUTPUT:  
Response code:  200  
Response JSON:  {'collab_number': 1, 'full_name': 'Bernardino', 'birth_date': '2020-11-12 00:00:00', 'current_salary': 999.99, 'active': True}  

**DELETE A COLLABORATOR**
```python
# Try to remove the collaborator
collab_number = 1
response = requests.delete(f'{COLLABORATORS_URL}/delete/{collab_number}')
```
OUTPUT:  
Response code:  200    
Response JSON:  {'Message': 'Successfully deleted'}  


