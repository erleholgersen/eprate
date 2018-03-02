#!/usr/bin/env python
# -*- coding: utf-8 -*-

### PREAMBLE ##################################################################
import argparse
import numpy as np

from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import cross_val_score, GridSearchCV
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

n_estimators = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 200, 500, 1000]
learning_rates = [0.005, 0.01, 0.02, 0.04, 0.05]




param_grid = [
	{'n_estimators':  n_estimators, 'learning_rate': learning_rates, 'loss': loss_functions}
	];

# for loss in loss_functions:
model = GridSearchCV(GradientBoostingRegressor(), param_grid, cv = 5)

model.fit(X, Y);

print model.best_params_




