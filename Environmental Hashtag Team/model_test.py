import gensim.downloader as api
from gensim.models.word2vec import Word2Vec
import inspect

# url: https://radimrehurek.com/gensim/auto_examples/howtos/run_downloader_api.html
print("Starting the code")
# Now, lets download the text8 corpus and load it to memory (automatically)
corpus = api.load('text8')

# Let's create a word2vec model of our corpus.
model = Word2Vec(corpus)

print(model.wv.most_similar('tree'))

print("Stopping the code")
