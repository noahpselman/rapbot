## creates song class

import re

class Song():

	def __init__(self, text):
		'''
		CONSTRUCTOR!!!!!!!!!
		'''
		self.raw_page = text

		self.find_song()
		self.find_artist()
		self.find_album()
		self.find_lyrics()
		# self.artist = None
		# self.album = None

	def find_song(self):
		line = re.findall(r"Song:.*", self.raw_page, flags=re.I)[0]
		self.title = ' '.join(line.split()[1:])


	def find_artist(self):
		line = re.findall(r"Artist:.*", self.raw_page, flags=re.I)[0]
		self.artist = ' '.join(line.split()[1:])
		

	def find_album(self):
		line = re.findall(r"Album:.*", self.raw_page, flags=re.I)[0]
		if line:
			self.album = ' '.join(line.split()[1:])
		else:
			self.album = None

	def find_lyrics(self):
		self.lyrics = '\n\n'.join(self.raw_page.split("\n\n")[1:])

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





