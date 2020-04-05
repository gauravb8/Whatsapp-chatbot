from flask import request
from flask import current_app as app
# import requests
import random
from twilio.twiml.messaging_response import MessagingResponse


def say_hi():
	return random.choice(app.responses_data.get_value('welcome_messages'))

def converse():
	incoming_msg = request.values.get('Body', '').lower()
	user_number = request.values.get('From','')
	print(user_number)
	print(request.values)
	print(request.values.get('From'))
	resp = MessagingResponse()
	msg = resp.message()
	responded = False
	welcome_msg = random.choice(app.responses_data.get_value('welcome_messages'))
	introduction = random.choice(app.responses_data.get_value('introduction_messages'))
	# print(Welcome_message)
	
	entities = app.wit_interface.get_response(incoming_msg)
	print(entities)
	
	if 'intent' in entities:
		if entities['intent'] == 'Welcome_message':
			msg.body(welcome_msg)
			responded = True
		if entities['intent'] == 'Introduction':
			msg.body(introduction)
			responded = True
	
		if entities['intent'] == 'Recommendation':
			if 'movie' in entities:
				text = "You want to watch movies like "+str(entities['movie'])+"."
				
			elif 'genre' in entities:
				text = "You want to watch "+str(entities['genre'])+" movies ."
			else:
				text = 'what type of movie you\'re looking for?'
			msg.body(text)
			responded = True
	
	if not responded:
		msg.body('My training is under process.')
	return str(resp)
	


	
# if __name__ =="__main__":
# 	app.run()