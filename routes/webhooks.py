from flask import Blueprint, request, jsonify

app = Blueprint('webhook', __name__)


@app.route("/webhook/", methods=['GET'])
def index():
    return "Webhooks: Server is running."


@app.route("/webhook/sms-status", methods=['POST'])
def sms_status():
    try:
        print("SMS status URL Response: ", request.json)
        return jsonify({})
    except Exception as exe:
        return jsonify({"status": 500, "error": exe})


@app.route("/webhook/inbound-sms", methods=['GET', 'POST'])
def inbound_sms():
    print("asa")
    if request.is_json:
        print(request.get_json())
    else:
        data = dict(request.form) or dict(request.args)
        print(data)

    return ('', 204)
