from flask import Blueprint, request, jsonify

# Create a Blueprint instance
app = Blueprint('webhooks', __name__)


@app.route("/webhook/", methods=['GET'])
def index():
    return "Webhook: Server is running."
