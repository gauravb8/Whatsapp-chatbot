from flask import request
from flask import current_app as app
# import requests
import random
from twilio.twiml.messaging_response import MessagingResponse
import requests
from urllib.parse import quote as urlencode


class BOTResponse(object):

	def __init__(self, phone_number):
		self.phone_number = phone_number
		if app.db.count_contexts(self.phone_number)==0:
			app.db.create_context(self.phone_number, '', [])

	def get_intent_response(self, intent, entity=None):
		if not entity:
			return random.choice(app.responses_data.get_value(intent)).format(intent)
		return random.choice(app.responses_data.get_value(intent)).format(entity) 

	def get_movie_info(self, title):
		try:
			url = 'http://www.omdbapi.com/?s={}&apikey=249bcab2'.format(urlencode(title))
			res = requests.get(url).json()
			return "{} ({})".format(res['Search'][0]['Title'], res['Search'][0]['Year'])
		except requests.exceptions.ConnectionError as err:
			print("Error while making OMDB API request: ", err)
			return ''

	def has_only_intent(self, intent):
		app.db.update_intent(self.phone_number, intent)
		return self.get_intent_response(intent)

	def has_only_entities(self, entities):
		app.db.add_entity_to_context(self.phone_number, entities)
		return self.get_intent_response(entities[0]['type'], entities[0]['value'])

	def has_intent_and_entities(self, intent, entities):
		app.db.update_intent(self.phone_number, intent)
		app.db.add_entity_to_context(self.phone_number, entities[0])
		return self.get_intent_response(entities[0]['type'], self.get_movie_info(entities[0]['value']))

	def no_intent_or_entities(self):
		return self.get_intent_response('no_match')


def converse():
	incoming_msg = request.values.get('Body', '').lower()
	user_number = request.values.get('From','').split(':')[1]
	# print(user_number)
	# print(request.values)
	# print(request.values.get('From'))
	# welcome_msg = random.choice(app.responses_data.get_value('welcome_messages'))
	# introduction = random.choice(app.responses_data.get_value('introduction_messages'))
	# print(Welcome_message)
	
	intent, entities = app.wit_interface.get_response(incoming_msg)
	print(intent, entities)
	
	bot_response = BOTResponse(user_number)

	if intent:
		if entities:
			response = bot_response.has_intent_and_entities(intent, entities)
		else:
			response = bot_response.has_only_intent(intent)

	else:
		response = bot_response.no_intent_or_entities()


	print(response)
	resp = MessagingResponse()
	resp.message().body(response)
	return str(resp)


	# if 'intent' in entities:
	# 	if entities['intent'] == 'Welcome_message':
	# 		msg.body(welcome_msg)
	# 		responded = True
	# 	if entities['intent'] == 'Introduction':
	# 		msg.body(introduction)
	# 		responded = True
	
	# 	if entities['intent'] == 'Recommendation':
	# 		if 'movie' in entities:
	# 			text = "You want to watch movies like "+str(entities['movie'])+"."
				
	# 		elif 'genre' in entities:
	# 			text = "You want to watch "+str(entities['genre'])+" movies ."
	# 		else:
	# 			text = 'what type of movie you\'re looking for?'
	# 		msg.body(text)
	# 		responded = True
	
	# if not responded:
	# 	msg.body('My training is under process.')
	# return str(resp)
	


	
# if __name__ =="__main__":
# 	app.run()