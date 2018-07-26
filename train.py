import csv
from collections import Counter
import math
import numpy as np
import matplotlib.pyplot as plt
import pandas
from re import sub
from decimal import Decimal

'''
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

	# Budget, Domestic, and Worldwide are in millions.
	# If in #x million format.
	if "million" in movie[6]:
		budget.append(float(movie[6].split()[0][1:]))
	else:
		budget_converter = sub(r'[^\d.]', '', movie[6])
		budget.append(float(budget_converter) / 1000000)

	# Domestic and worldwide box office grosses are in string format with $ and commas, which are annoying to deal with.
	domestic_converter = (sub(r'[^\d.]', '', movie[7]))
	domestic.append(float(domestic_converter) / 1000000.00)
	if movie[8] is not None and movie[8] is not '':
		worldwide_converter = (sub(r'[^\d.]', '', movie[8]))
	# If the movie was not released worldwide, we will just use its domestic  box office as its worldwide as well. 
	else:
		worldwide_converter = (sub(r'[^\d.]', '', movie[7]))
	worldwide.append(float(worldwide_converter) / 1000000.00)

print(budget)

plt.scatter(budget[:600], domestic[:600], s=5)
plt.show()

# Method 2 of gathering data from .csv.
names = ["title", "distributor", "release", "genre", "runtime", "rating", "budget", "domestic", "worldwide"]
dataset = pandas.read_csv("movie_data.csv", names=names)

# Take out category labels from movie data.
dataset = dataset[1:]
#print(dataset)
# x: budget; y: domestic
#plt.plot(array[:, 7], array[:, 6], "ro")
#plt.plot(array[:, 8], array[:,6], "bo")
#plt.show()
