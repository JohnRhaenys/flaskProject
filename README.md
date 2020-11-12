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


EXAMPLES:

LIST ALL COLLABORATORS:

```python
BASE_URL = 'http://127.0.0.1:5000'
COLLABORATORS_URL = f'{BASE_URL}/collaborators'

# List all collaborators
response = requests.get(f'{COLLABORATORS_URL}/all')
print('Response code: ', response.status_code)
print('Response JSON: ', response.json())
```

Output:  
Response code:  404  
Response JSON:  {'Error': 'No collaborators found'}  

LIST ALL COLLABORATORS IN A RANGE:
```python
# List all collaborators in a range of values (in this case, the API will return a JSON
# containing all collaborators with id between 0 and 10 (inclusively)
lower_bound = 0
upper_bound = 10
response = requests.get(f'{COLLABORATORS_URL}/all/{lower_bound}/{upper_bound}')
print('Response code: ', response.status_code)
print('Response JSON: ', response.json())
```
Output:  
Response code:  404  
Response JSON:  {'Error': 'No collaborators found'}  

