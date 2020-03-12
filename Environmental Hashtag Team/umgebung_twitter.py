# We add all the imports
import json
# Now we import wordnet from NTLK
from nltk.corpus import wordnet  #Import wordnet from the NLTK
# We import sentiwordnet
from nltk.corpus import sentiwordnet as swn


# This function returns the score of the tweet
def get_tweet_score(s):
	# We split the tweet by spaces to get each individual word.
	split_text = s.split()

	# We start by assigning 0 to the sentiment_score, this sentiment_score will consist of the sum of all
	# sentiment scores for each individual word.
	sentiment_score = 0  # sentiment_score

	# Here we specify the denominator that we will use to get the average
	# We will only take into account the words that have a score in wordnet.synsets
	syn_denominator = 0
	# We specify the overall score
	overall_score = 0

	# Now we iterate through each word to get the
	for w in split_text:
		synset = wordnet.synsets(w)
		# We check the length of the synset; we continue only if we get a response from wordnet.synsets
		if len(synset) > 0:
			# synset[0].name() contains the id that we will use to reference the word later in senti_synset
			# We assign this value to the variable name
			name = synset[0].name()
			# Below we get the positive and negative scores for the word using its name as id
			breakdown = swn.senti_synset(name)
			# We get the negative and positive scores
			pos_score = breakdown.pos_score()
			neg_score = breakdown.neg_score()

			# Then we calculate the sentiment_score for this word and add it up to the scores of the previous words.
			sentiment_score += neg_score - pos_score  # The sentiment_score of all words in the tweet.

			# We increase the syn_denominator count + 1
			syn_denominator += 1

	# Now we will calculate the average using syn_denominator as denominator
	if syn_denominator != 0:
		# Now we calculate the average and assign it to the overall_score
		# The overall_score will be the mean of each score
		overall_score = sentiment_score / syn_denominator

	# We return the tweet's overall_score.
	return overall_score


# Program starts here
print('Welcome to twitter hash tag processor!')
print('Starting program...')

# Here is a list that contains the names of the txt files that contain the twitter data
# Note: Txt files are not well-formed json files, each line contains a different json containing a tweet.
files_list = ['tweets_climatechange_06-03-2020', 'tweets_fridaysforfuture_09-03-2020', 'tweets_savetheplanet_09-03-2020']
# files_list = ['tweets_climatechange_06-03-2020_test', 'tweets_fridaysforfuture_09-03-2020_test', 'tweets_savetheplanet_09-03-2020_test']

# We iterate through all the files and extract the overall sentiment score for each individual tweet.
# Formula is overall_score = negative_score - positive_score; negative_score and positive_score are both integers >= 0.
# A >0 overall_score means a negative sentiment, while a <0 overall_score corresponds to a negative sentiment.
# A 0 overall_score reflects a neutral sentiment.
for file in files_list:
	# All files are txt files.
	f = open('Datasets/'+file+'.txt')
	# We read the lines of the txt file.
	lines = f.readlines()

	# We create the sentences dictionary. This will contain an array of sentences which each element will contain the
	# text and an overall score for the whole sentence.
	sentences = []

	# Counter for each sentence in the corpus, this is for later comparison with the file where we extracted the data.
	count = 0

	# For each line in the file we will proceed to
	for line in lines:
		# Data Extraction
		# We parse each fine of the file.
		parsed_json = (json.loads(line))

		# Discriminate to only take english sentences
		if parsed_json['lang'] == 'en':
			# We extract the text from the parsed line
			text = parsed_json['text']
			# We get the score for each sentence
			score = get_tweet_score(text)

			# Dictionary creation
			# We create a dictionary for the sentence
			sentences.append({
				'text': text,
				'score': score
			})

			# We increase the counter
			count += 1

	# We create a new file for each hash tag file that we consulted.
	with open('Results/'+file+'.json', 'w') as outfile:
		# We finally dump the tweets + the overall_score in a json file.
		json.dump(sentences, outfile)

# End of the program's execution
print("Total lines = "+str(count)+" we're processed.")
print("The program's execution has ended!")
