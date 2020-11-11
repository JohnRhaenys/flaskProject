from flask import jsonify

from exception_handling.my_exceptions import NotEnoughParametersException, InvalidParameterTypeException


class JSONValidator:

    @staticmethod
    def check_parameters(object, json_dict):
        missing_parameters = JSONValidator.get_missing_parameters(object=object, json_dict=json_dict)

        if missing_parameters:
            message = f'The following parameters are required: {str(missing_parameters)[1:-1]}'
            response_dict = {'Warning': message}
            response_json = jsonify(response_dict)
            raise NotEnoughParametersException(message=message, response_json=response_json)

        try:
            JSONValidator.validate_parameter_types(object=object, json_dict=json_dict)
        except InvalidParameterTypeException as e:
            raise InvalidParameterTypeException(message=e.message, response_json=e.response_json)

    @staticmethod
    def validate_parameter_types(object, json_dict):

        """
        Verifies whether the parameters respect the data types
        :param object: Collaborator or Sector
        :param json_dict: dictionary
        """
        types = object.get_types()

        for parameter_name in json_dict:
            function = types[parameter_name]
            parameter_value = json_dict[parameter_name]
            is_same_type, required_type = function(value=parameter_value)
            if not is_same_type:
                message = f"Wrong parameter type. Got '{type(parameter_value)}'. Expected {required_type}"
                response_dict = {'Error': message}
                response_json = jsonify(response_dict)
                raise InvalidParameterTypeException(message=message, response_json=response_json)

    @staticmethod
    def get_missing_parameters(object, json_dict):
        return [field for field in object.fields if json_dict.get(field) is None]
