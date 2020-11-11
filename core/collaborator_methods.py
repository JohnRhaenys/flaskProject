from flask import jsonify, Blueprint, request

from core import database

from validators.json_validator import JSONValidator
from exception_handling.my_exceptions import NotEnoughParametersException, InvalidParameterTypeException

from models.sector_model import Sector
from models.collaborator_model import collaborators_schema, Collaborator, collaborator_schema


collaborator_methods = Blueprint('collaborator_methods', __name__)


@collaborator_methods.route('/collaborators/add/<collab_number>', methods=['POST'])
def add(collab_number):
    """
    Inserts a new collaborator into the database
    :return: JSON string containing data about the collaborator
    """
    try:
        JSONValidator.check_parameters(object=Collaborator, json_dict=request.json)
    except NotEnoughParametersException as e:
        return e.response_json, 422
    except InvalidParameterTypeException as e:
        return e.response_json, 422

    # Check whether the collaborator does not already exist
    collaborator = Collaborator.query.filter_by(collab_number=collab_number).first()
    if collaborator:
        return jsonify({'Error': f'Collaborator already exists with number = {collab_number}'}), 409

    # Locate the sector based on its name
    sector_name = request.json['sector_name']
    sector = Sector.query.filter_by(name=sector_name).first()

    if not sector:
        return jsonify({'Error': f'Sector not found with name = {sector_name}'}), 409

    # Create an instance of Collaborator
    new_collaborator = Collaborator(
        collab_number=request.json['collab_number'],
        full_name=request.json['full_name'],
        birth_date=request.json['birth_date'],
        current_salary=request.json['current_salary'],
        active=request.json['active'],
        sector_name=sector_name,
    )
    new_collaborator.sector = sector

    # Persist the data
    database.insert(new_collaborator)

    return collaborator_schema.jsonify(new_collaborator), 200


@collaborator_methods.route('/collaborators/all', methods=['GET'])
def list_all_collaborators():
    """
    Lists the collaborators in the database ordered by name
    :return: JSON string containing data about all collaborators, if found. Else, a JSON string
    with an exception_handling message
    """
    all_collaborators = Collaborator.query.order_by(Collaborator.full_name).all()
    result = collaborators_schema.dump(all_collaborators)
    if not result:
        return jsonify({'Message': 'No collaborators registered'}), 404
    return jsonify(result)


@collaborator_methods.route('/collaborators/all/<name>', methods=['GET'])
def list_filtered_collaborators(name):
    """
    Lists the collaborators in the database filtered by name. In other words,
    returns one or more collaborators if the name given is a substring of any
     collaborator's name in the database
    :return: JSON string containing data about collaborators, if found. Else, a JSON string
    with an error message
    """
    try:
        JSONValidator.validate_parameter_types(object=Collaborator, json_dict={'full_name': name})
    except InvalidParameterTypeException as e:
        return e.response_json, 422

    all_collaborators = Collaborator\
        .query\
        .filter(Collaborator.full_name.like('%' + name + '%'))\
        .order_by(Collaborator.full_name).all()

    result = collaborators_schema.dump(all_collaborators)
    if not result:
        return jsonify({'Error': 'Not found'}), 404
    return jsonify(result), 200


@collaborator_methods.route('/collaborators/<collab_number>', methods=['GET'])
def get(collab_number):
    """
    Given the collab_number of a collaborator, queries the database
    :param collab_number: The id of the collaborator
    :return: JSON string containing data about the collaborator, if found. Else, a JSON string
    with an exception_handling message
    """
    # We try to parse the number
    try:
        collab_number = int(collab_number)
    except ValueError:
        return jsonify({'Error': f"The parameter '{collab_number}' cannot be parsed"}), 400

    # We try to find the collaborator
    collaborator = Collaborator.query.filter_by(collab_number=collab_number).first()

    # If the collaborator does not exist
    if not collaborator:
        return jsonify({'Error': f'Collaborator not found with id = {collab_number}'}), 404

    return collaborator_schema.jsonify(collaborator), 200


@collaborator_methods.route('/collaborators/update/<collab_number>', methods=['PUT'])
def update(collab_number):
    """
    Updates a collaborator in the database
    :param collab_number: The number of the collaborator
    :return: JSON string containing data about the collaborator, if found. Else, a JSON string
    with an exception_handling message
    """
    request_json = request.json

    try:
        JSONValidator.check_parameters(object=Collaborator, json_dict=request.json)
    except NotEnoughParametersException as e:
        return e.response_json, 422
    except InvalidParameterTypeException as e:
        return e.response_json, 422

    # We try to find the collaborator
    query = Collaborator.query.filter_by(collab_number=collab_number)
    collaborator = query.first()

    # If the collaborator does not exist
    if not collaborator:
        return jsonify({'Error': f'Collaborator not found with number = {collab_number}'}), 404

    # Locate the sector based on its name
    sector_name = request_json['sector_name']
    sector = Sector.query.filter_by(name=sector_name).first()

    if not sector:
        return jsonify({'Error': f'Sector not found with name = {sector_name}'}), 404

    # Reuse the request json to update the data
    tmp_json = request_json.copy()

    # Remove the sector_name field and add the sector_id field
    del tmp_json['sector_name']
    tmp_json['sector_id'] = collaborator.sector.id

    # Apply the changes and persist the data
    database.update(query=query, json=tmp_json)

    return jsonify(request_json), 200


@collaborator_methods.route('/collaborators/delete/<collab_number>', methods=['DELETE'])
def delete(collab_number):
    """
    Deletes a collaborator from the database
    :param collab_number: The number of the collaborator
    :return: JSON string containing data about the collaborator, if found. Else, a JSON string
    with an exception_handling message
    """
    try:
        JSONValidator.validate_parameter_types(object=Collaborator, json_dict=request.json)
    except InvalidParameterTypeException as e:
        return e.response_json, 422

    # We try to find the collaborator
    collaborator = Collaborator.query.filter_by(collab_number=collab_number)

    # If the collaborator does not exist
    if not collaborator:
        return jsonify({'Error': f'Collaborator not found with number = {collab_number}'}), 404

    # Delete the data and persist the changes
    database.delete(object=collaborator)

    return jsonify({'Message': 'Successfully deleted'}), 200
