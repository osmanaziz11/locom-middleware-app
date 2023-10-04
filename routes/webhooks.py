from flask import Blueprint, request, jsonify

app = Blueprint('webhook', __name__)


@app.route("/webhook/", methods=['GET'])
def index():
    return "Webhooks: Server is running."


@app.route("/webhook/answer", methods=['POST'])
def inbound_call():
    print(request.json)
    return jsonify([
        {
            "action": "talk",
            "text": "Welcome to a Vonage moderated conference. We will connect you when an agent is available",
            "voiceName": "Amy"
        },
    ]
    )
