from flask import current_app as app
from wit import Wit
import json



class WitInterface(object):

	def __init__(self, access_token):
		self.client = Wit(access_token = access_token)

	def get_response(self, text):
		res = self.client.message(text)
		confidence_threshold = {'intent': 0.6, 'movie':0.7, 'genre':0.7}

		print(res)
		intent, entities = '', []
		try:
			for key, val in res['entities'].items():
				if val[0]['confidence'] <= confidence_threshold[key]:
					continue
				if key=='intent':
					intent = val[0]['value']
				else:
					for entity in val:
						entities.append({'type': key, 'value': entity['value']})

		except KeyError as e:
			print("Key not found in Wit response: ", e)
		
		return (intent, entities)


class Data(object):

	def __init__(self, path):
		with open(path, 'r') as f:
			self.json_obj = json.load(f)

	def get_value(self, key):
		return self.json_obj.get(key, None)
		
		

