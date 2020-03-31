from wit import Wit



access_token = ""

client = Wit(access_token = access_token)

text = "suggest me some good movies"


def wit_response(text):
	resp = client.message(text)
	print(resp)
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


#print(wit_response(text))