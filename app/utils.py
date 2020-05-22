from flask import current_app as app
from wit import Wit
import json
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity



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

class Movies_Data(object):

	def __init__(self,path):
		self.df = pd.read_csv(path)
		self.features = ['keywords','cast','genres','director']

	def combine_features(self,row):
		all_features = ''
		for feature in self.features:
			all_features += str(row[feature])
		return all_features

	def get_title_from_index(self,index):
		return self.df[self.df.index == index]["title"].values[0]

	def get_popularityy_from_index(self,index):
		return self.df[self.df.index == index]["popularity"].values[0]

	def get_index_from_title(self,title):
		return self.df[self.df.title == title]["index"].values[0]


	def find_similar_movies(self,movie_user_likes):
		top_movies = {}
		for feature in self.features:
			self.df[feature] = self.df[feature].fillna('')

		tqdm.pandas()
		self.df["combined_features"] = self.df.progress_apply(self.combine_features,axis=1)
		cv = CountVectorizer()
		count_matrix = cv.fit_transform(self.df["combined_features"])
		cosine_sim = cosine_similarity(count_matrix)
		movie_index = self.get_index_from_title(movie_user_likes)
		similar_movies =  list(enumerate(cosine_sim[movie_index]))
		sorted_similar_movies = sorted(similar_movies,key=lambda x:x[1],reverse=True)[1:]
		top_movies = {self.get_title_from_index(sorted_similar_movies[i][0]):self.get_popularityy_from_index(sorted_similar_movies[i][0]) for i in range(10)}
		return  [name[0] for name in sorted(top_movies.items(), key=lambda x: x[1],reverse= True)]





		

