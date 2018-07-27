import csv
from collections import Counter
import math
import numpy as np
import matplotlib.pyplot as plt
import pandas
from re import sub
from decimal import Decimal
from sklearn.model_selection import train_test_split

'''
KEY:

0: title
1: distributor
2: release
3: genre
4: runtime
5: rating
6: budget
7: domestic
8: worldwide
'''

# Actual stuff goes here:
class bo_train:

	learning_rate = 0.0001
	epochs = 100


	# initialization
	def __init__(self):
		movie_data = self.load_data("movie_data.csv")
		budget, domestic, worldwide = self.get_parameters(movie_data)

		# For now, we'll do simple linear regression to predict domestic success, given budget.
		x_train, x_test, y_train, y_test = self.split_data(budget, domestic) # Can replace domestic with worldwide.

		#y = mx + b
		m, m_i, b, b_i = 1, 1, 0, 0
		e = [None] * bo_train.epochs


	# Loads data from csv file.
	def load_data(self, file):
		names = ["title", "distributor", "release", "genre", "runtime", "rating", "budget", "domestic", "worldwide"]
		dataset = pandas.read_csv(file, names=names)

		# Take out category labels from movie data.
		dataset = dataset[1:]

		values = dataset.values
		return values


	# From dataset we gather, extract only budget, domestic, worldwide gross
	def get_parameters(self, data):
		# Clean data; we don't want any movies without a budget or worldwide gross.
		bad_movies = []
		for i in range(len(data)):
			# Checking if the budget or worldwide gross are nan or unreadable.
			if data[i][6] != data[i][6] or data[i][8] != data[i][8] or 'xc2' in data[i][8]:
				bad_movies.append(i)
			else:
				# Reformatting budget.
				if "million" in movie[6]:
					data[i][6] = float(data[i][6].split()[0][1:])
				# If the budget is only in the thousands.
				else:
					budget_converter = sub(r'[^\d.]', '', data[i][6])
					data[i][6] = float(budget_converter) / 1000000

					# Reformating domestic and worldwide.
					domestic_converter = (sub(r'[^\d.]', '', data[i][7]))
					data[i][7] = float(domestic_converter) / 1000000.00

					worldwide_converter = (sub(r'[^\d.]', '', data[i][8]))
					data[i][8] = float(worldwide_converter) / 1000000.00

		# Delete bad stuff.
		data = np.delete(data, bad_movies, axis = 0)

		# Currently data is sorted in order by domestic gross.
		data = np.random.shuffle(data)

		# Get the stuff we want from the data.
		budget = data[:, 6]
		domestic = data[:, 7]
		worldwide = data[:, 8]

		return budget, domestic, worldwide


	# Split data into training set and testing set.
	def split_data(self, x, y):
		x_train, x_test, y_train, y_test = train_test_split(x, y, test=.2, train=.8, random_state=16)

		return x_train, x_test, y_train, y_test


# fun fun fun fun experiments
movies, title, distributor, release, genre, runtime, rating, budget, domestic, worldwide = [], [], [], [], [], [], [], [], [], []

# Read .csv file data into a 2d list.
with open('movie_data.csv', 'r') as f:
    file = csv.reader(f, delimiter=',', quotechar='"')
    for row in file:
        movies.append(row)

    # Take out category labels from movie data.
    movies = movies[1:]

# Separate the categories into their own lists.
for movie in movies:
	# If the movie doesn't have a listed budget, the movie won't help us with predictions.
	if movie[6] == "N/A":
		continue

	title.append(movie[0])
	distributor.append(movie[1])
	release.append(movie[2])
	genre.append(movie[3])
	runtime.append(movie[4])
	rating.append(movie[5])

	# Convert budget, domestic, and worldwide to millions.
	# If budget is in the millions.
	if "million" in movie[6]:
		budget.append(float(movie[6].split()[0][1:]))
	# If the budget is only in the thousands.
	else:
		budget_converter = sub(r'[^\d.]', '', movie[6])
		budget.append(float(budget_converter) / 1000000)

	# Domestic and worldwide box office grosses are in string format with $ and commas, which are annoying to deal with.
	domestic_converter = (sub(r'[^\d.]', '', movie[7]))
	domestic.append(float(domestic_converter) / 1000000.00)

	if movie[8] is not None and movie[8] is not '':
		worldwide_converter = (sub(r'[^\d.]', '', movie[8]))
	# If the movie was not released worldwide, we will just use its domestic box office as its worldwide for the sake of convenience. 
	else:
		worldwide_converter = (sub(r'[^\d.]', '', movie[7]))
	worldwide.append(float(worldwide_converter) / 1000000.00)

#print(budget)

#plt.scatter(budget[:700], domestic[:700], s=5)
#plt.show()


# some more functionality testing
names = ["title", "distributor", "release", "genre", "runtime", "rating", "budget", "domestic", "worldwide"]
dataset = pandas.read_csv("movie_data.csv", names=names)

		# Take out category labels from movie data.
dataset = dataset[1:]

values = dataset.values
for i in range(len(values)):
	domestic_converter = (sub(r'[^\d.]', '', values[i][7]))
	values[i][7] = float(domestic_converter) / 1000000.00

#print(values[:, 7])
