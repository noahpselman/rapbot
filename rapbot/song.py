## creates song class

import re

class Song():

	def __init__(self, text):
		'''
		CONSTRUCTOR!!!!!!!!!
		'''
		self.raw_page = text

		self.find_artist()
		self.find_album()
		self.find_lyrics()
		# self.artist = None
		# self.album = None

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


class Verse():
	
	def __init__(self, text, song_artist):

		self.text = text


	def find_artist(self):
		snip = re.search(r'\[.*\]|\(.*\)|:', self.lyrics.split('\n')[0])
		
		if snip

		if re.match(r"[.*\]")





