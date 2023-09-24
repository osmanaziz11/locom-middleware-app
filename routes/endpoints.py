from flask import Blueprint

# Create a Blueprint instance
app = Blueprint('api', __name__)


@app.route("/", methods=['GET'])
def index():
    return "Endpoints: Server is running."
