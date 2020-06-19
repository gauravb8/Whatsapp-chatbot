from flask import request
from flask import current_app as app
# import requests
import random
from twilio.twiml.messaging_response import MessagingResponse
import requests
from urllib.parse import quote as urlencode

class MovieAPI(object):
	def __init__(self):
		self.url = 'http://www.omdbapi.com/?s={}&apikey=249bcab2'
		self.imdb_root_url = 'https://imdb.com/title/'

	def get_movie_info(self, title):
		try:
			res = requests.get(self.url.format(title)).json()
			top_result = res['Search'][0]
			return "{} ({})\n{}".format(top_result['Title'], top_result['Year'], self.imdb_root_url+top_result['imdbID']), top_result['Poster']
		except requests.exceptions.ConnectionError as err:
			print("Error while making OMDB API request: ", err)
			return ''


class BOTResponse(object):

	def __init__(self, phone_number):
		self.phone_number = phone_number
		if app.db.count_contexts(self.phone_number)==0:
			app.db.create_context(self.phone_number, '', [])
		self.movie_api = MovieAPI()

	def get_intent_response(self, intent, entity=None):
		if not entity:
			return random.choice(app.responses_data.get_value(intent)).format(intent)
		return random.choice(app.responses_data.get_value(intent)).format(entity) 


	def has_only_intent(self, intent, temp_intent = None):
		if temp_intent == "hi_again":
			print("inside hi again")
			app.db.update_intent(self.phone_number, intent)
			return self.get_intent_response(temp_intent)
		app.db.update_intent(self.phone_number, intent)
		return self.get_intent_response(intent)

	def has_only_entities(self, entities):
		app.db.add_entity_to_context(self.phone_number, entities)
		return self.get_intent_response(entities[0]['type'], entities[0]['value'])

	def has_intent_and_entities(self, intent, entities):
		app.db.update_intent(self.phone_number, intent)
		app.db.add_entity_to_context(self.phone_number, entities[0])
		recommendations = list(map(self.movie_api.get_movie_info, app.movie_info.find_similar_movies(entities[0]['value'])))
		# recommendations = '\n'.join(["{}. {}".format(i+1,name) for i,name in enumerate(app.movie_info.find_similar_movies(entities[0]['value']))]) 
		return recommendations
		# return self.get_intent_response(entities[0]['type'], recommendations)
	
		
	def is_hi_again(self,phone_number,intent):
		context = app.db.get_context(self.phone_number)
		if 'intent' in context:
			if intent == context['intent'] and intent in ("Welcome_message","Introduction"):
				return True
		return False
		
	def no_intent_or_entities(self):
		return self.get_intent_response('no_match')


def format_response(res):
	response = MessagingResponse()
	if isinstance(res, list):
		for movie, poster in res:
			msg = response.message()
			msg.body(movie)
			msg.media(poster)
	elif isinstance(res, str):
		msg = response.message()
		msg.body(res)

	return str(response)

def converse():
	incoming_msg = request.values.get('Body', '').lower()
	user_number = request.values.get('From','').split(':')[1]
	
	intent, entities = app.wit_interface.get_response(incoming_msg)
	print(intent, entities)
	
	bot_response = BOTResponse(user_number)

	if intent:
		if entities:
			response = bot_response.has_intent_and_entities(intent, entities)
		else:
			if bot_response.is_hi_again(user_number,intent):
				response = bot_response.has_only_intent(intent,"hi_again")
			else:
				response = bot_response.has_only_intent(intent)

	else:
		response = app.chat_bot.get_response(str(incoming_msg), user_number)
		#response = bot_response.no_intent_or_entities()

	print(response)

	return format_response(response)

