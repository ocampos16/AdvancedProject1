# We do the import for the word embedding
import gensim.downloader as api
from gensim.models import Word2Vec, KeyedVectors
import numpy as np

class WordEmbedding:

	def __init__(self):
		print("Loading word embedding")
		self.model = KeyedVectors.load_word2vec_format('Corpus\GoogleNews-vectors-negative300.bin.gz', binary=True, limit=100000)
		# self.corpus = api.load('text8')
		# self.model = Word2Vec(self.corpus)
		print("Word2Vec loaded successfully!")

	def get_most_similars(self, word=""):
		print("Running word embedding")
		# Now, lets download the text8 corpus and load it to memory (automatically)
		# self.corpus = api.load('text8')

		# Let's create a word2vec model of our corpus.
		# self.model = Word2Vec(self.corpus)

		# We get the most similar words for a given word
		most_similars = self.model.most_similar(word)


		# We return a list with the most similar words
		return most_similars
