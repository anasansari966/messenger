from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

VERIFY_TOKEN = "mySuperSecretToken12345"
PAGE_ACCESS_TOKEN = "EAAUPhdUnufUBO83A6ASLUy9GDibZCD175akYFPJWAjiaJWX3zXxSSFUAYcB5qOrw0hZB21IwRZBM1DXX80pkvQphqovvL8mEUgcxpT4R5oaezjzsfhc9WcAL12lvGXglCovjwxSdyIpuGKYVnfN4PRsY4prZAbLil7FyawCgAUWIt8S6rQkZAEMpIrx8NYIqn"

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/webhook', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    for entry in data['entry']:
        for messaging_event in entry['messaging']:
            if 'message' in messaging_event:
                sender_id = messaging_event['sender']['id']
                message_text = messaging_event['message']['text']
                response_text = get_response(message_text)
                send_message(sender_id, response_text)
    return "ok", 200

def get_response(message_text):
    if "operating hours" in message_text.lower():
        return "We are open from 9 AM to 5 PM, Monday to Friday."
    elif "services" in message_text.lower():
        return "We offer web development, mobile app development, and digital marketing services."
    else:
        return "Sorry, I didn't understand that. Please ask about our operating hours or services."

def send_message(recipient_id, message_text):
    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    }
    r = requests.post("https://graph.facebook.com/v13.0/me/messages", params=params, headers=headers, json=data)
    return r.json()

if __name__ == "__main__":
    app.run()