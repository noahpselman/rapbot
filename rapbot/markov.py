import random
import database

WORDS_PER_BAR = 10

class word_block():

	def __init__(self, k):

		self.contents = []
		self.k = k


	def add(self, element):

		self.contents.append(element)
		if len(self.contents) > self.k:
			del self.contents[0]


	def populate(self, words):
		# print(words)
		if len(words)!=self.k:
			print(words)

		assert len(words)==self.k

		for w in words:
			self.add(w)


	def is_full(self):
		return len(self.contents) == self.k


	def to_tup(self):
		return tuple(self.contents)


	def __repr__(self):

		return ' '.join(self.contents)



class Model():

	def __init__(self, training_data, k):
		'''
		training data is list of lyrics objects (which are just strings)
		'''

		self.k = k
		self.training_data = training_data
		self.openers = []
		self.first_words = []
		self.word_model = {}
		self.rhyme_model = {}


	def build_word_model(self):

		for i, song in enumerate(self.training_data):
			print("song number:", i)
			words = song.split()

			if len(words) < self.k:
				continue

			self.openers.append(words[:self.k])
			block = word_block(self.k)
			block.populate(words[:self.k])

			for word in words[self.k:]:

				key = block.to_tup()
				self.word_model[key] = self.word_model.get(key, []) + [word]

				block.add(word)



class Rapper():
	"""
	purpose is to generate songzz
	"""

	def __init__(self, Model):

		self.Model = Model


	def spit_verse(self, num_bars=16):

		bars = []
		bar_count = 0
		prev_bar = None
		
		while bar_count < num_bars:

			bar = self.spit_bar(prev_bar=prev_bar)

			bars.append(bar)
			prev_bar = bar
			bar_count += 1

		self.recent_verse = bars

		# return bars



	def spit_bar(self, prev_bar=None):

		block = word_block(self.Model.k)
		bar = []
		
		if prev_bar:
			block.populate(prev_bar[-self.Model.k:])

		else:
			bar.extend(random.choice(self.Model.openers))
			block.populate(bar)

		while len(bar) < WORDS_PER_BAR:

			new_word = self.choose_word(prev_k=block.to_tup())
			bar.append(new_word)
			block.add(new_word)

		# print(' '.join(bar))
		return bar


	def print_verse(self):

		text = [' '.join(line) for line in self.recent_verse]
		print('\n'.join(text))		


			

		

	def choose_word(self, prev_k):


		word = random.choice(self.Model.word_model[prev_k])

		return word




def build_training_data():

	cnx = database.get_cnx()
	table = database.pull_table(cnx, ['lyrics'], 'clean_text')

	return [l[0] for l in table]

