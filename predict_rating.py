#!/usr/bin/env python
# -*- coding: utf-8 -*-

### PREAMBLE ##################################################################
import argparse
import pandas as pd
import numpy as np

import os, sys

from collections import Counter

from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

from sklearn.ensemble import RandomForestRegressor

### PARAMETERS ################################################################

parser = argparse.ArgumentParser()

parser.add_argument('show', help = 'Term to search for on IMDB')
parser.add_argument('new_description', help = 'Description to predict')
args = parser.parse_args()

show = args.show
new_description = args.new_description

threshold = 3


### FUNCTIONS #################################################################

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


### OPEN DATA #################################################################

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

### TOKENIZE ##################################################################

tokenizer = RegexpTokenizer(r'\w+')
all_tokens = tokenizer.tokenize( ' '.join(episode_data['plot']).lower() )

# remove stop words
all_tokens = [token for token in all_tokens if token not in stopwords.words('english')]

token_counts = Counter(all_tokens)

features = token_counts

for key in list(features):
	if features[key] < threshold: 
		del features[key]


# convert plots to indicator variables for each feature
episode_tokens = []

for plot in episode_data['plot']:

	feature_indicators = make_indicators(plot, features)
	episode_tokens.append(feature_indicators)

### FIT MODEL #################################################################

X = pd.DataFrame(episode_tokens, columns = features.keys(), index = episode_data['title'])
Y = episode_data['rating']

rf_model = RandomForestRegressor()
rf_model = rf_model.fit(X, Y)

### PREDICT ###################################################################

r = make_indicators(new_description, features)

predicted_rating = rf_model.predict( np.array(r).reshape(1, -1) )

print predicted_rating




