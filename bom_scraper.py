import sys
import bs4
from urllib.request import urlopen
import re

# Return list of movie links for boxofficemojo.com.
def load_links():
	# We start on page 1 of all time domestic box office results.
	current_url = "http://www.boxofficemojo.com/alltime/domestic.htm?page=1&p=.htm"

	# Initialize as empty list, to contain URLs to individual movies.
	movie_links = []

	# Contains partial links (text after http://www.boxofficemojo.com).
	partial_links = []

	# From page 1 to page 10, we collect all of the links to the movies we find.
	for i in range(1, 11):
		current_url = "http://www.boxofficemojo.com/alltime/domestic.htm?page={}&p=.htm".format(i)

		soup = bs4.BeautifulSoup(urlopen(current_url).read(), 'lxml')

		# Find all clickable links (these will result in extraneous links, but we'll find all the movie links too).
		stuff = soup.find_all('a', href=True) 

		for part_link in stuff:
			# If it is a link to a movie, add it to partial_links list.
			if part_link.get('href')[0:12] == '/movies/?id=' and part_link.get('href') not in partial_links:
				partial_links.append(part_link.get('href'))

	#print(partial_links)

	# We have 939 movies to work with.
	#print(len(partial_links))

	for link in partial_links:
		movie_links.append("http://www.boxofficemojo.com" + link)
	#print(movie_links)
	return movie_links

def get_movie_data(link):
	pass


def write_csv():
	pass

# testing:
url = "http://www.boxofficemojo.com/movies/?id=starwars7.htm"
soup = bs4.BeautifulSoup(urlopen(url).read(), 'lxml')
print(soup)


