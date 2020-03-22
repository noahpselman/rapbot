import re
import urllib.parse
import util
from bs4 import BeautifulSoup

STARTING_URL = "http://ohhla.com/YFA_eminem.html"
LIMITING_DOMAIN = "ohhla.com"
# SESSION = requests.Session()
# SESSION.trust_env = False



def open_page(url):

	# print("opening...", url)
	r = util.get_request(url)

	# print("r:", r)

	if r:
		return r.url, BeautifulSoup(util.read_request(r))

	else:
		return None, None


def is_artist_page(soup):

	trs = soup.find_all('tr')
	artist_page = any([re.search(r'all artists database', t.text, flags=re.I) for t in trs])
	# print(artist_page)
	return artist_page


def get_artists(soup):

	artists = []

	### check if page has artist
	if is_artist_page(soup):
		### collect artist names
		artist_tags = soup.find('pre').find_all('a')

		for tag in artist_tags:
			if tag.text.strip():
				artists.append(tag.text)

		# artists = map(lambda x: x.text, artist_tags)
		# print(artists)
	# print("hi")
	return artists


# def get_lyrics(current_page, soup, visited_pages=set()):
def get_lyrics(url, visited_pages=set()):

	print("\ntrying", url)
	visited_pages.add(url)
	print("visited_pages length: {}".format(len(visited_pages)))

	try:
		url, soup = open_page(url)

	except Exception:
		print("there was an exception\n")
		return []

	if not url:
		print("no url")
		return []

	## base case
	if url[-4:] == '.txt':# or len(visited_pages) > 2:
		print("adding {}\n".format(url))
		return [url]

	## recursive case
	else:
		# print("reached recursive case")
		lyrics = []
		new_links = soup.find_all('a')

		for link in new_links:

			### check if link can be followed
			if 'href' not in link.attrs:
				print("href not in attrs")
				continue
			
			# print(link['href'])

			clean_link = util.remove_fragment(link['href'])
			# print("link: {}".format(clean_link))

			if not clean_link:
				print("no clean link")
				continue
			
			abs_link = util.convert_if_relative_url(url, clean_link)

			if abs_link in visited_pages or not util.is_url_ok_to_follow(abs_link, LIMITING_DOMAIN) or 'update' in abs_link:
				print("child link shan't be followed: {}".format(abs_link))
				continue

			lyrics += get_lyrics(abs_link, visited_pages)

		return lyrics
	# print(url)


