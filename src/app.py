from expert_system import *
from exception import InvalidUsage
from validations import validate_fields
from flask import Flask, request, jsonify

#Imported objects from testing env
model = Expert()

app = Flask(__name__)

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    """
    Handles any error raised by the other methods
    """
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route('/')
def home_endpoint():
    return "Welcome to the ECOVALUE's expert system API!"


@app.route('/recommend', methods=['POST'])
def get_prediction():
    # Works only for a single sample
    if request.method == 'POST':
        entry = request.get_json()  # Get data posted as a json
        if validate_fields(entry):
            model.set_facts(entry)
            model.run()
            response = jsonify(model.answer)
            return response
        raise InvalidUsage("""
Unprocessable entity, 
check all the required fields are present and comply with the rules.
Contact admin for more info.
""", 422)
    raise InvalidUsage("Method Not Allowed", 405)


if __name__ == '__main__':
    preprocess()  # load model at the beginning once only
    app.run(host='0.0.0.0', port=80)
