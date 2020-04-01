import json
# Import my own python files
from word_embedding import WordEmbedding
import numpy as np

# Python code to sort the tuples using second element
# of sublist Function to sort using sorted()
def Sort(sub_li):
	# reverse = None (Sorts in Ascending order)
	# key is set to sort using second element of
	# sublist lambda has been used
	return (sorted(sub_li, key=lambda x: x[1], reverse=True))

# This is the main file of the project
def main(url="None"):
	# We create an instance of the word embedding
	wemb = WordEmbedding()

	# We define a data
	dataset = None

	# We will open the file(s)
	with open(url) as json_file:
		dataset = json.load(json_file)
		for data in dataset:
			d = data.get("text", "")
			print(d)

			# We get the words in the sentences
			words = d.split()

			# We get a dictionary to relate the words to their most similars
			embedded_text = ""

			# We iterate for each word and we get the word embedding
			for w in words:
				# We check if the word embedding produces results.
				# similars_list = wemb.get_most_similars(w)
				# print(similars_list)
				try:
					similars_list = wemb.get_most_similars(w)
					# We sort the list
					sorted_list = Sort(similars_list)
					np_array = np.array(sorted_list)

					embedded_text += np_array[0,0] + " "
				except:
					# We concatenate the original word in case we coudln't find it in the word embedding
					embedded_text += w + " "

			data['embedded_text'] = embedded_text
			print("We have ended searching the words")

		# new URL
		new_url = new_url = url.split("/")[1].split(".")[0]
		# We create a new file for each hash tag file that we consulted.
		with open('Embedded_Results/' + new_url + "_embedded" + '.json', 'w') as outfile:
			# We finally dump the tweets + the overall_score in a json file.
			json.dump(dataset, outfile)

	# w_embedding.run()
	print("Exiting main")


if __name__ == "__main__":
	print("Program started")
	# We will continue with the word embedding
	files = ['Results/tweets_climatechange_06-03-2020.json', 'Results/tweets_fridaysforfuture_09-03-2020.json', 'Results/tweets_savetheplanet_09-03-2020.json']

	for f in files:
		main(url=f)

	print("End of the program")
