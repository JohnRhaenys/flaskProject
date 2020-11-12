from flask import jsonify

from exception_handling.my_exceptions import NotEnoughParametersException, InvalidParameterTypeException


class JSONValidator:
    """
    Class used to validate the parameters from the requests
    """

    @staticmethod
    def check_parameters(object_model, json_dict):
        missing_parameters = JSONValidator.get_list_of_missing_parameters(object_model=object_model, json_dict=json_dict)
        if missing_parameters:
            message = f'The following parameters are required: {str(missing_parameters)[1:-1]}'
            response_dict = {'Warning': message}
            response_json = jsonify(response_dict)
            raise NotEnoughParametersException(message=message, response_json=response_json)

        try:
            JSONValidator.validate_parameter_types(object_model=object_model, json_dict=json_dict)
        except InvalidParameterTypeException as e:
            raise InvalidParameterTypeException(message=e.message, response_json=e.response_json)

    @staticmethod
    def get_list_of_missing_parameters(object_model, json_dict):
        return [field for field in object_model.fields if json_dict.get(field) is None]

    @staticmethod
    def validate_parameter_types(object_model, json_dict):
        """
        Verifies whether the parameters respect the data types
        """

        # Retrieve the dictionary which contains the list
        # of attributes of the object_model and their respective types
        types = object_model.get_types()

        # Verify whether every JSON parameter type matches the object_model's attributes types
        for parameter_name in json_dict:
            function = types[parameter_name]
            parameter_value = json_dict[parameter_name]
            is_same_type, required_type = function(value=parameter_value)
            if not is_same_type:
                message = f"Wrong parameter type. Got '{type(parameter_value)}'. Expected {required_type}"
                response_dict = {'Error': message}
                response_json = jsonify(response_dict)
                raise InvalidParameterTypeException(message=message, response_json=response_json)
