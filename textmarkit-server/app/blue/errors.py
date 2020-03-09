from flask import Blueprint, jsonify, make_response

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(Exception)
def handle_error(error):

	status_code = 500
	success = False
	response = {
		'success': success,
		'error': {
			'type': 'Unexpected Exception',
			'message': 'An unexpected error has occured.'
		}
	}

	return make_response(jsonify(response), status_code)
