import re
import urllib.parse
import util
from bs4 import BeautifulSoup

STARTING_URL = "http://ohhla.com/favorite.html"
LIMITING_DOMAIN = "ohhla.com"
# SESSION = requests.Session()
# SESSION.trust_env = False
BAD_TAGS = ['left', 'left-wrap', 'menu']

ADD_RAW_TEXT = (
	"INSERT INTO raw_text "
	"(url, text) "
	"VALUES (%s, %s) "
	)

def verify_no_menu(tag):

	tag.descendents


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
def get_lyrics(cnx, cursor, url=STARTING_URL, visited_pages=set()):

	print("\ntrying", url)
	visited_pages.add(url)
	print("visited_pages length: {}".format(len(visited_pages)))

	try:
		url, soup = open_page(url)

	except Exception:
		print("there was an exception - you done fucked up\n")
		return None

	if not url:
		print("no url")
		return None

	## base case
	if url[-4:] == '.txt':# or len(visited_pages) > 2:
		if soup.find('pre'):
			text = soup.find('pre').text
			print("adding {}\n".format(url))
		else:
			ps = soup.find_all('p')
			ps = list(filter(lambda x: 'Artist:' in x.text, ps))
			if len(ps)==1:
				text = ps[0].text
			else:
				text = soup.text

		cursor.execute(ADD_RAW_TEXT, (url, text))
		cnx.commit()
		# return [(url, text)]

	## recursive case
	else:
		# print("reached recursive case")
		lyrics = []
		if soup.find('div', id='leftmain'):
			tag = soup.find('div', id='leftmain')
		else:
			tag = soup
		new_links = tag.find_all('a', href=True)

		for link in new_links:

			# if len(visited_pages) > 30:
			# 	continue

			### check if link can be followed
			# if 'href' not in link.attrs:
			# 	print("href not in attrs")
			# 	continue
			
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

			get_lyrics(cnx, cursor, abs_link, visited_pages)

		# return None
	# print(url)


