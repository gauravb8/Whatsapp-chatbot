from flask import current_app as app
from wit import Wit
import json



class WitInterface(object):

	def __init__(self, access_token):
		self.client = Wit(access_token = access_token)

	def get_response(self, text):
		resp = self.client.message(text)
		# return str(resp)
		Values = {}
		
		try:
			for key,value in resp['entities'].items():
				Values[key] = value[0]['value']
				
			
		except:
			pass
		
		return Values

class Data(object):

	def __init__(self, path):
		with open(path, 'r') as f:
			self.json_obj = json.load(f)

	def get_value(self, key):
		return self.json_obj.get(key, None)
		
		

