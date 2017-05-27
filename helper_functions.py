from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

from collections import Counter

import pandas as pd

import os, sys

def make_indicators(string, features, tokenizer = RegexpTokenizer(r'\w+')):
	""" 
	Convert string to indicator vector for each word in features.

	:param string: string to be converted
	:param features: Counter object containing features to be included 
	:param tokenizer: nltk tokenizer object to split string

	"""

	string_tokens = tokenizer.tokenize( string.lower() )

	indicators = []

	for feature in features.keys(): 
		in_string = feature in string_tokens

		indicators.append( int(in_string) )

	return(indicators)


def load_data(show):
	"""
	Load data on show

	:param show: string giving TV show

	"""

	show_name_string = '_'.join(show.lower().split())

	filepath = os.path.join('data', show_name_string + '_episodes.tsv')

	if not os.path.isfile(filepath):
		error_message = "Sorry, I can't find episode data for " + args.show + '\n' 
		error_message += 'Have you tried running gather_data.py?'

		sys.exit(error_message)

	episode_data = pd.read_table(
		os.path.join('data', show_name_string + '_episodes.tsv'), 
		encoding = 'utf-8',
		sep = '\t'
		)

	return episode_data


def tokenize_episodes(episode_plots, threshold = 3, remove_stop_words = True):
	"""
	Convert episode plots to token representation

	:param episode_plots: 
	:param threshold: recurrence threshold for word to 
	:param remove_stop_words: boolean indicating if stop words should be removed. 

	"""

	tokenizer = RegexpTokenizer(r'\w+')
	all_tokens = tokenizer.tokenize( ' '.join(episode_plots).lower() )

	# remove stop words if requested
	if remove_stop_words:
		all_tokens = [token for token in all_tokens if token not in stopwords.words('english')]
	
	token_counts = Counter(all_tokens)

	features = token_counts

	for key in list(features):
		if features[key] < threshold: 
			del features[key]

	# convert plots to indicator variables for each feature
	episode_tokens = []

	for plot in episode_plots:

		feature_indicators = make_indicators(plot, features)
		episode_tokens.append(feature_indicators)

	return episode_tokens, features