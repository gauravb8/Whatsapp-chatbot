from flask import current_app as app
import pymongo
from urllib.parse import quote as urlencode


class DataBase(object):
	def __init__(self, connection_string, username, password):
		self.client = pymongo.MongoClient(connection_string.format(urlencode(username), urlencode(password)))

