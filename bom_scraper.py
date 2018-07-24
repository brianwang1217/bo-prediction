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
#print(soup)

# Gets the table of stats that we want for the linked movie.
stuff = soup.select_one('div.mp_box table')

# Domestic gross.
#print(stuff.find('b', text='Domestic:').find_next('td').text)
# Worldwide gross.
#print(stuff.find('b', text='Worldwide:').find_next('td').text)

# Director
director = soup.find_all('a', href = re.compile('Director&id'))
#print (director[0].encode_contents())

# A lot of important information we want is in bolded text.
bolded_text = soup.find_all('b')

# Empty list initialized to store all of the data that we want to keep.
info_list = []

for data in bolded_text:
	#print (data)

	# Unnecessary information.
	if 'Domestic Lifetime' not in str(data.encode_contents()):
		info_list.append(str(data.encode_contents()))

# Make sure this is a domestic release.
if '$' in info_list[2] and 'n/a' not in info_list[9]:
	title = info_list[1]
	domestic = info_list[2]

	# warning: this might be None; if it is not:
	if 'n/a' not in info_list[3]:
		distributor = info_list[3].split('>')[1].split('<')[0]

	# sometimes release date is not in hyperlink.
	if len(info_list[4].split('>')) > 3:
		release = info_list[4].split('>')[2].split('<')[0]
	else:
		release = info_list[4].split('>')[1].split('<')[0]

	genre = info_list[5]
	runtime = info_list[6]
	rating = info_list[7]
	budget = info_list[8]

	# If movie was released worldwide.
	if 'n/a' not in info_list[13] and '$' in info_list[13]:
		worldwide = info_list[13]
	else:
		worldwide = None

#print(distributor, release, worldwide)

# We've got everything we want EXCEPT for *opening weekend*... 
# Now we have to clean data AND code.
