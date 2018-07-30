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

	# initialization
	def __init__(self, epochs=500):
		movie_data = self.load_data("movie_data.csv")
		budget, domestic, worldwide = self.get_parameters(movie_data)

		# For now, we'll do simple linear regression to predict domestic success, given budget.
		x_train, x_test, y_train, y_test = self.split_data(budget, domestic) # Can replace domestic with worldwide.

		y_train = self.transform(y_train)
		y_test = self.transform(y_test)

		#y = mx + b
		m, b = 1, 0

		# Track error thoughout epochs.
		error_list = []

		error_list.append(self.error(x_train, y_train, m, b))

		for i in range(epochs):
			m, b = self.lr_gradient_step(x_train, y_train, m, b)
			error_list.append(self.error(x_train, y_train, m, b))

		test_error = self.error(x_test, y_test, m, b)

		# Print final error, as well as test_error.
		print(error_list[-1], test_error)	

		# Graph time!
		self.graph_error(error_list)
		self.graph_model(x_train, y_train, m, b, epochs)


	# Loads data from csv file.
	def load_data(self, file):
		names = ["title", "distributor", "release", "genre", "runtime", "rating", "budget", "domestic", "worldwide"]
		dataset = pandas.read_csv(file, names=names)

		# Take out category labels from movie data.
		dataset = dataset[1:]

		return dataset.values


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
				if "million" in data[i][6]:
					data[i][6] = float(data[i][6].split()[0][1:])
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

		# Get the stuff we want from the data.
		budget = data[:, 6]
		domestic = data[:, 7]
		worldwide = data[:, 8]

		return budget, domestic, worldwide


	# Split data into training set and testing set.
	def split_data(self, x, y):
		x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=.2, train_size=.8, random_state=16)

		return x_train, x_test, y_train, y_test


	# MSE
	def error(self, x, y, m, b):
		num_vals = len(x)
		sum = 0 
		for i in range(num_vals):
			sum += (y[i] - (m*x[i] + b)) ** 2
		return sum / float(num_vals)


	# Approach 1

	# summations of x, y, xy, x^2, y^2
	def get_lr_stats(self, x, y):
		sum_x, sum_y, sum_xy, sum_xx, sum_yy = sum(x), sum(y), 0, 0, 0
		num_vals = len(x)
		for i in range (num_vals):
			sum_xy += x[i] * y[i]
			sum_xx += x[i] ** 2
			sum_yy += y[i] ** 2
		return sum_x, sum_y, sum_xy, sum_xx, sum_yy

	# lr performance
	# slope, y-intercept
	def lr(self, x, y):
		lr_stats = self.get_lr_stats(x, y)
		b = (lr_stats[1] * lr_stats[3] - lr_stats[0] * lr_stats[2]) / float(len(x) * lr_stats[3] - lr_stats[0] ** 2)
		m = (len(x) * lr_stats[2] - lr_stats[0] * lr_stats[1]) / float(len(x) * lr_stats[3] - lr_stats[0] ** 2)
		return m, b


	# Approach 2

	# Gradient steps
	def lr_gradient_step(self, x, y, m_current, b_current, learning_rate = 0.00001):
		n = float(len(x))
		b_gradient = 0
		m_gradient = 0

		for i in range(len(x)):
			b_gradient += -(2/n) * (y[i] - ((m_current * x[i]) + b_current))
			m_gradient += -(2/n) * x[i] * (y[i] - ((m_current * x[i]) + b_current))

		new_b = b_current - (learning_rate * b_gradient)
		new_m = m_current - (learning_rate * m_gradient)
		return new_m, new_b

	# Data is a bit skewed; let's apply a y^.125 transformation to improve accuracy. 
	def transform(self, y):
		return np.sqrt(np.sqrt(np.sqrt(y.astype(float))))


	def graph_model(self, x, y, m, b, epochs):
		plt.scatter(x, y, s=2)
		plt.xlabel('Budget (millions)')
		plt.ylabel('Domestic Gross (millions^.125)')
		plt.plot(x, m*x + b, label='trained model')
		plt.title("Trained model with {} epochs".format(epochs))
		plt.show()


	def graph_error(self, error_list):
		x = range(len(error_list))
		y = error_list
		plt.scatter(x, y, s=2)
		plt.xlabel('Epoch')
		plt.ylabel('MSE (y^.125)')
		plt.title('Error per epoch')
		plt.show()


p = bo_train()

'''
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
'''