from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)


@app.route('/bot', methods=['POST'])
def bot():
	incoming_msg = request.values.get('Body', '').lower()
	resp = MessagingResponse()
	msg = resp.message()
	responded = False
	if 'hi' in incoming_msg:
		msg = 'hello'
		msg.body(msg)
		responded = True
	if 'hello' in incoming_msg:
		msg = 'hey'
		msg.body(msg)
		responded = True
	if not responded:
		msg.body('My training is under process.')
	return str(resp)