from flask import Blueprint

app = Blueprint('webhook', __name__)


@app.route("/webhook/", methods=['GET'])
def index():
    return "Webhooks: Server is running."
