from flask import Blueprint, request, jsonify

# Create a Blueprint instance
app = Blueprint('endpoints', __name__)


@app.route("/api/", methods=['GET'])
def index():
    return "API: Server is running."
