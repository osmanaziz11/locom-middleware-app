from flask import Blueprint, request, jsonify

app = Blueprint('webhook', __name__)


@app.route("/webhook/", methods=['GET'])
def index():
    return "Webhooks: Server is running."


@app.route("/webhook/answer", methods=['GET', 'POST'])
def index():
    print(request.json)
    return jsonify([
        {
            "action": "talk",
            "text": "Hello from voange"
        }
    ]
    )
