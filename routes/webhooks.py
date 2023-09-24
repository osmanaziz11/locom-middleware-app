from flask import Blueprint, request

app = Blueprint('webhook', __name__)


@app.route("/webhook/", methods=['GET'])
def index():
    return "Webhooks: Server is running."


@app.route("/inbound-sms", methods=['GET', 'POST'])
def inbound_sms():
    print("asa")
    if request.is_json:
        print(request.get_json())
    else:
        data = dict(request.form) or dict(request.args)
        print(data)

    return ('', 204)
