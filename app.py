from routes.endpoints import app as endpoints
from routes.webhooks import app as webhooks
from flask import Flask

app = Flask(__name__)
app.register_blueprint(endpoints)
app.register_blueprint(webhooks)


