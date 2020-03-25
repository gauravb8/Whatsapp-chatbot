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
	if 'hi' in incoming_msg.lower():
		msg.body('hello')
		responded = True
	if 'hello' in incoming_msg.lower():
		msg.body('Wassup')
		responded = True
	if '?' in incoming_msg:
		msg.body("Well I'm glad you asked. I am a chat bot developed to service your needs. Go on and enter your query.")
		responded = True
	if not responded:
		msg.body('My training is under process.')
	return str(resp)

if __name__ == '__main__':
	app.run()