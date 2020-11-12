from flask import jsonify, Blueprint, request

from database import database
from models.sector_model import Sector, sectors_schema, sector_schema

sector_methods = Blueprint('sector_methods', __name__)


@sector_methods.route('/sectors/add/<string:sector_name>', methods=['POST'])
def add(sector_name):
    """
    Inserts a new sector into the database
    :param sector_name: The name of the sector (Tecnologia de Informacao, Financas ...)
    :return: JSON string containing data about the sector, if added successfully.
    Else, a JSON string with an error message
    """
    # Validate the json
    errors = sector_schema.validate(request.json)
    if errors:
        return jsonify(errors), 422

    # Check whether the Sector does not already exist
    sector = Sector.query.filter_by(name=sector_name).first()
    if sector:
        return jsonify({'Error': f'Sector already exists with name = {sector_name}'}), 409

    # Create a new Sector and persist the data
    new_sector = Sector(name=request.json['name'])
    database.insert(new_sector)

    return sector_schema.jsonify(new_sector), 200


@sector_methods.route('/sectors/all', methods=['GET'])
def list_all_sectors():
    """
    Lists the sectors in the database (ordered by name)
    :return: JSON string containing data about all sectors, if found.
    Else, a JSON string with an error message
    """
    all_sectors = Sector.query.order_by(Sector.name).all()
    result = sectors_schema.dump(all_sectors)
    if not result:
        return jsonify({'Error': 'No sectors found'}), 404
    return jsonify(result)


@sector_methods.route('/sectors/all/<string:name>', methods=['GET'])
def list_sectors_filtered_by_name(name):
    """
    Lists the sectors in the database filtered by name
    :param name: The name to be matched
    :return: JSON string containing data about all sectors, if found.
    Else, a JSON string with an error message
    """
    all_sectors = Sector\
        .query\
        .filter(Sector.name.like('%' + name + '%'))\
        .order_by(Sector.name).all()

    result = sectors_schema.dump(all_sectors)
    if not result:
        return jsonify({'Message': 'No sectors registered'}), 404
    return jsonify(result), 200


@sector_methods.route('/sectors/<string:name>', methods=['GET'])
def get(name):
    """
    Tries to get a sector from the database
    :param name: The name of the sector
    :return: JSON string containing data about the sector, if found.
    Else, a JSON string with an error message
    """
    sector = Sector.query.filter_by(name=name).first()
    if not sector:
        return jsonify({'Error': f'Sector not found with name = {name}'}), 404
    return sector_schema.jsonify(sector), 200


@sector_methods.route('/sectors/update/<string:sector_name>', methods=['PUT'])
def update(sector_name):
    """
    Updates a sector in the database
    :param sector_name: The name of the sector
    :return: JSON string containing data about the sector, if found.
    Else, a JSON string with an error message
    """
    request_json = request.json
    errors = sector_schema.validate(request_json)
    if errors:
        return jsonify(errors), 422

    # Check whether the Sector does not already exist
    query = Sector.query.filter_by(name=sector_name)
    sector = query.first()
    if not sector:
        return jsonify({'Error': f'Sector not found with name = {sector_name}'}), 404

    # Update and persist the changes
    database.update(query=query, json=request_json)

    return jsonify(request.json), 200


@sector_methods.route('/sectors/delete/<string:sector_name>', methods=['DELETE'])
def delete(sector_name):
    """
    Deletes a sector from the database
    :param sector_name: The name of the sector
    :return: JSON string containing a success message, if the sector has been deleted.
    Else, a JSON string with an error message
    """
    # Check whether the Sector exists
    sector = Sector.query.filter_by(name=sector_name).first()

    if not sector:
        return jsonify({'Error': f'Sector not found with name = {sector_name}'}), 404

    # Delete the data and persist the changes
    database.delete(the_object=sector)

    return jsonify({'Message': 'Successfully deleted'}), 200
