import requests as re
import urllib.parse
import util
from bs4 import BeautifulSoup

STARTING_URL = "http://ohhla.com/YFA_eminem.html"
LIMITING_DOMAIN = "ohhla.com"
# SESSION = requests.Session()
# SESSION.trust_env = False


def is_absolute_url(url):
	'''
	Is url an absolute URL?
	'''
	if url == "":
		return False
	return urllib.parse.urlparse(url).netloc != ""


def get_request(url):

	if is_absolute_url(url):

		try:
			r = re.get(url)
			if r.status_code == 404 or r.status_code == 403:
				r = None
		
		except Exception:
			# fail on any kind of error
			r = None

		return r


def read_request(request):

	try:
		return request.text.encode('iso-8859-1')

	except Exception:
		print("read failed: " + request.url)

	return ""


def convert_if_relative_url(current_url, new_url):
    '''
    Attempt to determine whether new_url is a relative URL and if so,
    use current_url to determine the path and create a new absolute
    URL.  Will add the protocol, if that is all that is missing.

    Inputs:
        current_url: absolute URL
        new_url:

    Outputs:
        new absolute URL or None, if cannot determine that
        new_url is a relative URL.

    Examples:
        convert_if_relative_url("http://cs.uchicago.edu", "pa/pa1.html") yields
            'http://cs.uchicago.edu/pa/pa.html'

        convert_if_relative_url("http://cs.uchicago.edu", "foo.edu/pa.html")
            yields 'http://foo.edu/pa.html'
    '''
    if new_url == "" or not is_absolute_url(current_url):
        return None

    if is_absolute_url(new_url):
        return new_url

    parsed_url = urllib.parse.urlparse(new_url)
    path_parts = parsed_url.path.split("/")

    if not path_parts:
        return None

    ext = path_parts[0][-4:]
    if ext in [".edu", ".org", ".com", ".net"]:
        return "http://" + new_url
    elif new_url[:3] == "www":
        return "http://" + new_path
    else:
        return urllib.parse.urljoin(current_url, new_url)


def open_page(url):

	# print("opening...", url)
	r = util.get_request(url)

	# print("r:", r)

	if r:
		return r.url, BeautifulSoup(util.read_request(r))

	else:
		return None, None
	# 	return BeautifulSoup(read_request(get_request(url)))

	# else:
	# 	return BeautifulSoup(read_request(get_request(new_url)))


		

	 #    try:
		#     return BeautifulSoup(r.text.encode('iso-8859-1'))
		
		# except Exception:
		#     print("read failed: " + r.url)
		
	 #    return ""

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







def visit_page(url, limiting_domain, visited_courses, map_dict, filename):

	r = util.get_request(url)
	current_url = util.get_request_url(r)
	soup = soupify(util.read_request(r))


def get_links(page):
	return list_of_links

