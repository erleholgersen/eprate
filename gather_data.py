#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import argparse
import csv
from imdb import IMDb
import os

### SORT OUT COMMAND LINE ARGUMENTS ###########################################

parser = argparse.ArgumentParser(description = 'Download episode data from IMDB.')

parser.add_argument('search_term', help = 'Term to search for on IMDB')
args = parser.parse_args()

search_term = args.search_term

### FUNCTIONS #################################################################
def get_top_tv_show(search_results):
	""" Return top search result which is a TV show """

	top_result = None

	for i in range(0, len(search_results) - 1):
		if 'tv series' == search_results[i]['kind']:
			top_result = search_results[i]
			break

	return top_result


### GET DATA ##################################################################

# initalize database
db = IMDb()

search_results = db.search_movie(search_term)

#! check that you actually get correct result
# take top result which is a TV show
#! this is not the most robust approach - re-consider.
top_result = get_top_tv_show(search_results)

# let user know what's happening
print('Downloading data on', top_result['title'])


# get more info
db.update(top_result, ['main', 'episodes'])


### PROCESS EPISODE DETAILS ###################################################

season_numbers, episode_numbers, titles, plots, ratings = [], [], [], [], []

for season_number, season_details in top_result['episodes'].items():
	for episode_number, episode_details in season_details.items():

		# only keep the ones with a rating
		if not 'rating' in episode_details.keys():
			continue

		season_numbers.append(episode_details['season'])
		episode_numbers.append(episode_details['episode'])

		ratings.append(episode_details['rating'])

		titles.append(episode_details['title'].replace('\n', ''))
		plots.append(episode_details['plot'].replace('\n', ''))


# make pandas data frame
dic = {'season': season_numbers, 'episode': episode_numbers, 'title': titles, 'plot': plots, 'rating': ratings }
episodes = pd.DataFrame(dic)

# restrict to main seasons, not interested in prequels
episodes = episodes[episodes.season > 0]

### SAVE ############################################################££££££££££

filename = '_'.join(search_term.lower().split()) + '_episodes.tsv'

episodes.to_csv(
	os.path.join('data', filename), 
	sep = '\t', 
	encoding = 'utf-8', 
	quoting = csv.QUOTE_NONNUMERIC, 
	index = False)


