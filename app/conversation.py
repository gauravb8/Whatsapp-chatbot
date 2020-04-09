import os
import aiml
from flask import current_app as app
import random
#from autocorrect import spell
class Conversation(object):

	def __init__(self, BRAIN_FILE,learnFiles):
		self.aiml_kernel = aiml.Kernel()
		if os.path.exists(BRAIN_FILE):
			print("Loading from brain file: " + BRAIN_FILE)
			self.aiml_kernel.loadBrain(BRAIN_FILE)
		else:
			print("Parsing aiml files")
			self.aiml_kernel.bootstrap(learnFiles=learnFiles, commands="load aiml")
			print("Saving brain file: " + BRAIN_FILE)
			self.aiml_kernel.saveBrain(BRAIN_FILE)

	
	def get_response(self,query):
		emojis = ["😅","😀","😃","😄","😋","😛","😝","😂","😅","🥵","😭","😬","😑"]

		query = [w for w in (query.split())]
		response = self.aiml_kernel.respond(query)
		if response:
			return str(response)
		else:
			return (str(random.choice(emojis)))