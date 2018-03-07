### PREAMBLE ##################################################################
import argparse
import numpy as np

import h2o
from h2o.automl import H2OAutoML

from helper_functions import *

### PARAMETERS ################################################################
# Sort out command line arguments
#
parser = argparse.ArgumentParser()
parser.add_argument('show', help = 'Term to search for on IMDB')
args = parser.parse_args()

show = args.show
threshold = 0 

### MAIN ######################################################################

# start h2o instance
h2o.init()

# get data
episode_data = load_data(show)
episode_tokens, features = tokenize_episodes(episode_data['plot'], threshold = threshold)

X = pd.DataFrame(episode_tokens, columns = features.keys(), index = episode_data['title'])


# convert to AutoML format - need predictors and response in same object
X_h2o = h2o.H2OFrame( X.assign(rating = episode_data.rating.values ) )

# get names of predictor columns
predictors = X_h2o.columns;
predictors.remove('rating');

# fit model
models = H2OAutoML(max_runtime_secs = 30)
models.train(
    x = predictors,
    y = 'rating',
    training_frame = X_h2o,
    )

print( models.leaderboard )

