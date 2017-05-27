#!/usr/bin/env python
# -*- coding: utf-8 -*-

### PREAMBLE ##################################################################
import argparse
import numpy as np

from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_absolute_error, make_scorer

from helper_functions import *

### PARAMETERS ################################################################

parser = argparse.ArgumentParser()

# parser.add_argument('show', help = 'Term to search for on IMDB')
# parser.add_argument('new_description', help = 'Description to predict')
# args = parser.parse_args()

# show = args.show
# new_description = args.new_description

show = 'Doctor Who'

threshold = 3

### PREPARE DATA ##############################################################

episode_data = load_data(show)
episode_tokens, features = tokenize_episodes(episode_data['plot'], threshold = threshold)

X = pd.DataFrame(episode_tokens, columns = features.keys(), index = episode_data['title'])
Y = episode_data['rating']

### TEST MODELS ###############################################################

model = RandomForestRegressor()
left_out = LeaveOneOut()

scores = cross_val_score(model, X, Y, cv = 5, scoring = make_scorer(mean_absolute_error))
print scores

