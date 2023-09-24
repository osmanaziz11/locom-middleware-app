from flask import Blueprint

# Create a Blueprint instance
app = Blueprint('webhook', __name__)


@app.route("/webhook/", methods=['GET'])
def index():
    return "Webhooks: Server is running."
