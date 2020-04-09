from flask import current_app as app
import pymongo
from pymongo.errors import WriteError, PyMongoError
from urllib.parse import quote as urlencode
from datetime import datetime, timedelta


class DataBase(object):
	CONTEXT_VALIDITY_MINS = 10
	def __init__(self, connection_string, username, password):
		print('Connecting to DB..')
		self.client = pymongo.MongoClient(connection_string.format(urlencode(username), urlencode(password)), connect=True)
		print('Connected!')

	def set_context_collection(self, dbname, collection_name):
		self.contexts = self.client[dbname][collection_name]

	def create_context(self, phone_number, intent, entities):
		try:
			object_id = self.contexts.insert_one({
				'phone_number': phone_number,
				'timestamp': datetime.now(),
				'intent': intent,
				'entities': entities
				})
			print("Successfully created context with object_id: ", object_id)
			return object_id
		except WriteError as e:
			print('Error while inserting document: ', e)

	def get_context(self, phone_number):
		try:
			chat_context = self.contexts.find_one({
				'phone_number': phone_number,
				'timestamp': {'$gt': datetime.now() - timedelta(minutes=self.CONTEXT_VALIDITY_MINS)}
				})
			if chat_context is None:
				print('No context exists for number: ',phone_number)
			return chat_context
		except PyMongoError as e:
			print("Error: ", e)

	def count_contexts(self, phone_number):
		try:
			return self.contexts.count_documents({
				'phone_number': phone_number,
				'timestamp': {'$gt': datetime.now() - timedelta(minutes=self.CONTEXT_VALIDITY_MINS)}
				})
		except PyMongoError as e:
			print('PyMongoError: ', e)

	# def add_entity_to_context(self, phone_number, entity):
	# 	try:
	# 		return self.contexts.update_one({
	# 			'phone_number': phone_number,
	# 			'entities.type': {'$ne': entity['type']}}, {
	# 			'$addToSet': {"entities": entity}
	# 			})
	# 	except WriteError as e:
	# 		print('Error while updating document: ', e)

	def update_intent(self, phone_number, intent):
		try:
			return self.contexts.update_one({
				'phone_number': phone_number
				}, {
				'$set': {'intent': intent}
				})
		except PyMongoError as e:
			print('PyMongoError: ', e)

	def add_entity_to_context(self, phone_number, entity):
		try:
			# If entity already exists, update its value
			if self.contexts.update_one({
				'phone_number': phone_number,
				'entities.type': entity['type']
				}, {
				'$set': {'entities.$.value': entity['value']}
				}).matched_count == 0:
				# Existing entity of same type not found, insert a new one
				self.contexts.update_one({
					'phone_number': phone_number
					}, {
					'$addToSet': {"entities": entity}
					})
		except PyMongoError as e:
			print("PyMongoError: ", e)

	def delete_context(self, phone_number):
		try:
			return self.contexts.delete_one({'phone_number': phone_number})
		except PyMongoError as e:
			print('Error: ', e)

	# def all_entities_gathered(self, phone_number)


