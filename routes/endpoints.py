from flask import Blueprint, make_response
from util.twilio import TwilioManager

app = Blueprint('api', __name__)

# Define common error responses


@app.route("/", methods=['GET'])
def index():
    return "Endpoints: Server is running."


@app.route("/api/numbers/<country_code>", methods=['GET'])
def view_numbers(country_code):
    try:
        twilio_manager = TwilioManager()
        response = twilio_manager.get_available_numbers(country_code)
        if isinstance(response, str):
            return make_response(response, 401)  # 401 for Unauthorized
        else:
            # If it's a successful response, return it with the 200 status code
            return make_response(str(response), 200)
    except Exception as exe:
        return make_response(str(exe), 500)  # 500 for Internal Server Error
