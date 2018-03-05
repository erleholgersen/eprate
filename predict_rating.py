#!/usr/bin/env python
# -*- coding: utf-8 -*-

### PREAMBLE ##################################################################
import argparse
import numpy as np

from sklearn.ensemble import GradientBoostingRegressor

from helper_functions import *

### PARAMETERS ################################################################

parser = argparse.ArgumentParser()

parser.add_argument('show', help = 'Term to search for on IMDB')
parser.add_argument('new_description', help = 'Description to predict')
args = parser.parse_args()

show = args.show
new_description = args.new_description

threshold = 10

### PREPARE DATA ##############################################################

episode_data = load_data(show)
episode_tokens, features = tokenize_episodes(episode_data['plot'], threshold = threshold)

X = pd.DataFrame(episode_tokens, columns = features.keys(), index = episode_data['title'])
Y = episode_data['rating']

gb_model = GradientBoostingRegressor(n_estimators = 100, loss = 'lad')
gb_model = gb_model.fit(X, Y)

### PREDICT ###################################################################

r = make_indicators(new_description, features)

predicted_rating = gb_model.predict( np.array(r).reshape(1, -1) )

print(predicted_rating)




