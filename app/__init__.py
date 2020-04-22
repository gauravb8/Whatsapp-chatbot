import os

from flask import Flask


def create_app(test_config=None):
	# create and configure the app
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_pyfile('config.py')

	
	# a simple page that says hello
	@app.route('/hello')
	def hello():
		return 'Hello, World! ' + app.config['TWILIO_AUTH_TOKEN']

	project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	print('Project dir: ', project_dir)

	# Attach shared objects to app context
	from app import utils, bot, db, conversation
	app.wit_interface = utils.WitInterface(app.config['WIT_AUTH_TOKEN'])
	app.responses_data = utils.Data(os.path.join(project_dir, 'data', 'bot_answers.json'))
	app.db = db.DataBase(app.config['MONGO_CONNECTION_STRING'], app.config['MONGO_USERNAME'], app.config['MONGO_PASSWORD'])
	app.db.set_context_collection(app.config['MONGO_BOT_DB'], app.config['MONGO_CONTEXT_COLLECTION'])
	app.chat_bot = conversation.Conversation(os.path.join(project_dir, app.config['BRAIN_FILE']), os.path.join(project_dir, app.config['LEARN_FILES']))
	# Routes
	# app.add_url_rule('/bot', 'bot_intro', bot.say_hi, methods=['GET'])
	app.add_url_rule('/bot', 'bot_response', bot.converse, methods=['POST'])


	return app
