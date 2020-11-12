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
