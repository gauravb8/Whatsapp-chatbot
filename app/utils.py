from flask import current_app as app
from wit import Wit
import json



class WitInterface(object):

	def __init__(self, access_token):
		self.client = Wit(access_token = access_token)

	def get_response(self, text):
		resp = self.client.message(text)
		# return str(resp)
		entity = None
		value = None
		intent = None
		intent_value = None
		entity_value = None
		
		try:
			entity = list(resp['entities'])[0] #'movie'
			if entity == 'movie':
				entity_value = resp['entities'][entity][0]['value']
				intent = list(resp['entities'])[1]
				intent_value = resp['entities'][intent][0]['value']
			else:
				entity = None
				entity_value = None
				intent = list(resp['entities'])[0]
				intent_value = resp['entities'][intent][0]['value']
				
			
		except:
			pass
		
		return(intent_value,entity,entity_value)


class Data(object):

	def __init__(self, path):
		with open(path, 'r') as f:
			self.json_obj = json.load(f)

	def get_value(self, key):
		return self.json_obj.get(key, None)
