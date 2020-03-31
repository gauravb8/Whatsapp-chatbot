from flask import Flask, request
import requests
import random
from utils import wit_response
from read_answers import get_messages
from twilio.twiml.messaging_response import MessagingResponse
from configparser import ConfigParser


app = Flask(__name__)


@app.route('/bot', methods=['POST'])
def bot():
	incoming_msg = request.values.get('Body', '').lower()
	resp = MessagingResponse()
	msg = resp.message()
	responded = False
	file_name = "bot_answers.json"
	data = get_messages(file_name)
	print(data)
	Welcome_message = data['intent']['Welcome_message'][0]['value']
	Introduction = data['intent']['Introduction'][0]['value']
	print(Welcome_message)
	
	intent_value,entity,entity_value = wit_response(str(incoming_msg))
	print(intent_value)
	print(entity)
	print(entity_value)
	
	if intent_value == 	'Welcome_message':
		text = str(random.choice(Welcome_message))
		msg.body(text)
		responded = True
		
	if intent_value == 	'Introduction':
		text = str(random.choice(Introduction))
		msg.body(text)
		responded = True
	
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