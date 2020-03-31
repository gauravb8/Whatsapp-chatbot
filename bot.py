from flask import Flask, request
import requests
from utils import wit_response
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)


@app.route('/bot', methods=['POST'])
def bot():
	incoming_msg = request.values.get('Body', '').lower()
	resp = MessagingResponse()
	msg = resp.message()
	responded = False
	if 'hi' in incoming_msg:
		text = 'Hello!'
		msg.body(text)
		responded = True
	if 'hello' in incoming_msg:
		text = 'Hey!'
		msg.body(text)
		responded = True
	if 'are you' in incoming_msg:
		text = "Well I'm glad you asked. I am a chat bot developed to service your needs. Go on and enter your query."
		msg.body(text)
		responded = True
		
	intent_value,entity,entity_value = wit_response(str(incoming_msg))
	print(intent_value)
	print(entity)
	print(entity_value)
	
		
	if intent_value == 'Recommendation':
		if entity == None:
			text = 'What kind of movies do you want to watch?'
		else:
			text =  "You want to watch movies like "+str(entity_value)+"."
		msg.body(text)
		responded = True
	
	if not responded:
		msg.body('My training is under process.')
	return str(resp)
	


	
if __name__ =="__main__":
	app.run()