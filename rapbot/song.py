## creates song class
## used for parsing scraped text into artists, albums, and lyrics
## challenge is finding standardized artist identification for each verse

import re

class Song():

	def __init__(self, text):
		'''
		CONSTRUCTOR!!!!!!!!!
		'''
		self.raw_page = text

		self.find_song(text)
		self.find_artist(text)
		self.find_album(text)
		self.find_lyrics(text)
		# self.artist = None
		# self.album = None

	def find_song(self, text):
		lines = re.findall(r"Song:.*", text, flags=re.I)
		if lines:
			self.title = ' '.join(lines[0].split()[1:])
		else:
			self.title = ""


	def find_artist(self, text):
		lines = re.findall(r"Artist:.*", text, flags=re.I)
		if lines:			
			self.artist = ' '.join(lines[0].split()[1:])
		else:
			self.artist = ""
		

	def find_album(self, text):
		lines = re.findall(r"Album:.*", text, flags=re.I)
		if lines:
			self.album = ' '.join(lines[0].split()[1:])
		else:
			self.album = ""

	def find_lyrics(self, text):

		lyrics = re.sub(r"[\(\[].*?[\)\]]", "", text)  ### remove brackets and parens
		lyrics = re.sub(r"[^\w\s:]", "", lyrics)
		lyrics = re.findall(r"^[^:\n]*?$", lyrics, flags=re.MULTILINE)
		lyrics = filter(lambda x: x.strip(), lyrics)
		lyrics = '\n'.join(list(lyrics))
		self.lyrics = lyrics.lower()
			# ^()\[\]:].*", text, flags=re.MULTILINE)
		# return re.sub(r"[^()\[\]:].*", text, flags=re.MULTILINE))


	def __repr__(self):

		title = "Title: {}".format(self.title)
		artist = "Arist: {}".format(self.artist)
		album = "Album: {}".format(self.album)

		s = '\n'.join([title, artist, album])

		return s


class Verse():
	
	def __init__(self, text, song, song_artist, verse_artist=None):

		self.text = text
		self.song = song
		self.song_artist = song_artist
		self.verse_artist = verse_artist

		if not verse_artist:
			self.find_verse_artist()


	def find_verse_artist():
		artist_line = re.findall(r'\[.*\]|\(.*\)', line)

		if len(artist_line) == 1:			
			self.verse_artist = artist_line[0][1:-1]


		if len(artist_line) > 1:
			self.verse_artist = artist_line[0][1:-1]			
			
			for a in artist_line[1:]:
				v = Verse(self.text, self.song, self.song_artist, self.verse_artist)

		else:
			### Check if artist is in artist list
			self.verse_artist = self.song_artist

		




	# def find_artist(self):
	# 	snip = re.search(r'\[.*\]|\(.*\)|:', self.lyrics.split('\n')[0])
		
	# 	if snip

	# 	if re.match(r"[.*\]")





