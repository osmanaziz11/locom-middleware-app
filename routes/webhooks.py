from flask import Blueprint, request
from util.firebase import FirebaseManager
from util.twilio import TwilioManager


app = Blueprint('webhook', __name__)


@app.route("/webhook/", methods=['GET'])
def index():
    return "Webhooks: Server is running."


@app.route("/webhook/answer", methods=['POST'])
def inbound_call():
    firebase = FirebaseManager()
    twilio = TwilioManager()
    response = request.json
    if response['status'] == 'un-answered':
        frwd_number = firebase.get_forwarded_number(response['to'])
        if frwd_number != None:
            isBlackListed = firebase.blacklist_check(
                response['to'], response['from'])
            if not isBlackListed:
                if firebase.check_conversation_take_over(response['to'], response['from']):
                    return_message = twilio.sendMessage(
                        response['to'], response['from'], 'Some Message')
                    if isinstance(return_message, dict):
                        firebase.add_message(
                            response['to'], response['from'], return_message)
