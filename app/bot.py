from flask import request
from flask import current_app as app
# import requests
import random
from twilio.twiml.messaging_response import MessagingResponse


def say_hi():
	return random.choice(app.responses_data.get_value('welcome_messages'))

def converse():
	incoming_msg = request.values.get('Body', '').lower()
	resp = MessagingResponse()
	msg = resp.message()
	responded = False
	welcome_msg = random.choice(app.responses_data.get_value('welcome_messages'))
	introduction = random.choice(app.responses_data.get_value('introduction_messages'))
	# print(Welcome_message)
	
	intent_value,entity,entity_value = app.wit_interface.get_response(incoming_msg)
	print(intent_value, entity, entity_value)
	
	if intent_value == 	'Welcome_message':
		msg.body(welcome_msg)
		responded = True
		
	if intent_value == 'Introduction':
		msg.body(introduction)
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
	


	
# if __name__ =="__main__":
# 	app.run()