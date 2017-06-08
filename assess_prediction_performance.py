#!/usr/bin/env python
# -*- coding: utf-8 -*-

### PREAMBLE ##################################################################
import argparse
import numpy as np

from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import cross_val_score
from sklearn.metrics import make_scorer, mean_squared_error, mean_absolute_error

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

scorer = make_scorer(mean_squared_error)

loss_functions = ['ls', 'lad', 'huber', 'quantile']
n_estimators = [20, 50, 100, 200, 500]

for loss in loss_functions:
    for n in n_estimators:
        model = GradientBoostingRegressor(loss = loss, n_estimators = n, learning_rate = 0.05)
        scores = cross_val_score(model, X, Y, cv = 5, scoring = scorer)
        print loss, n, np.mean(scores)
