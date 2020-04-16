# We add all the imports
import json # Import json to handle json files.
from nltk.corpus import wordnet  #Import wordnet from the NLTK
from nltk.corpus import sentiwordnet as swn # We import sentiwordnet

# Import libraries needed for data cleaning
import emoji
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

def Data_Cleaning(lines):
    # Define a dictioary of emoticons
    dict_emo = { ':-)'  : b'\xf0\x9f\x98\x8a',
                      ':)'   : b'\xf0\x9f\x98\x8a',
                      '=)'   : b'\xf0\x9f\x98\x8a',  # Smile or happy
                     ':-D'  : b'\xf0\x9f\x98\x83',
                      ':D'   : b'\xf0\x9f\x98\x83',
                      '=D'   : b'\xf0\x9f\x98\x83',  # Big smile
                      '>:-(' : b'\xF0\x9F\x98\xA0',
                      '>:-o' : b'\xF0\x9F\x98\xA0'   # Angry face
                      }
    #Function converts emoticons to emoji
    def convert_emoticons(emoticons):
        emoticons=emoticons.replace('.',' ')
        emoticons=emoticons.replace(',',' ')
        for i in emoticons.split():
            if i in dict_emo.keys():
                word=dict_emo[i].decode('utf-8')
                emoticons=emoticons.replace(i,word)
        return emoticons

    #Function to convert emoji to word
    def convert_emoji_to_word(emo_converted_text):
        for i in emo_converted_text:
            if i in emoji.UNICODE_EMOJI:
                emo_word=str(emoji.demojize(i))
                rep_colon=emo_word.replace(':',' ')
                rep_dash=rep_colon.replace('_',' ')
                emo_converted_text=emo_converted_text.replace(i,rep_dash)
        return emo_converted_text
    # Function tokenizes the whole data, normalies it to lower case, removes
    #stop words and stems the data
    def clean_data(text):
        tokens= word_tokenize(text)
        # convert to lower case
        tokens = [w.lower() for w in tokens]
        # remove all tokens that are not alphabetic
        words = [word for word in tokens if word.isalpha()]
        # filter out stop words
        stop_words = set(stopwords.words('english'))
        words = [w for w in words if not w in stop_words]
        porter = PorterStemmer()
        stemmed = [porter.stem(word) for word in words]
        return stemmed

    # Task of data Cleaning function starts here
    text=str(lines)
    text=text.replace("ufeff"," ")
    text=text.replace("'","")
    emoticons_treated=convert_emoticons(text)
    emo_treated_lines=convert_emoji_to_word(emoticons_treated)
    cleaned_text=clean_data(emo_treated_lines)
    # The final cleaned text is ready for word embedding
    return set(cleaned_text)

# Test sentence to check that everything is working fine.
# lines="I am very happy :). Have a nice day 👍. Also, I miss you :), take care😘! I can't leave."
# word_embed=Data_Cleaning(lines)
# print(word_embed)

def get_hypernyms(tweet):

    new_tweet = tweet

    # We create a counter to iterate through each word
    counter = 0
    # Now we iterate through each word to get the
    for w in tweet:
        synset = wordnet.synsets(w)

        # We check the length of the synset; we continue only if we get a response from wordnet.synsets
        if len(synset) > 0:
            # We get the hypernym
            hyper = synset[0].hypernyms()
            # If we get a result
            if len(hyper) > 0:
                first_lemma = hyper[0]
                lemmas = first_lemma.lemma_names()
                new_tweet[counter] = lemmas[0]

        # We increase the counter
        counter += 1

    return new_tweet

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

    # Now we replace each for in the tweet for its hypernym
    split_text = get_hypernyms(split_text)

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
    return overall_score, split_text


# Next we iterate through all the files and assign a score
def assign_scores(files_list):
	for file in files_list:
		# All files are txt files.
		f = open('Datasets/' + file + '.txt')
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

				# Now we proceed to clean the text
				cleaned_set = Data_Cleaning(text)
				after_clean_text = " ".join(cleaned_set)

				# Now we iterate and we take the hypernyms of each word
				# We get the score for each sentence
				score, hypernyms = get_tweet_score(after_clean_text)

				# Dictionary creation
				# We create a dictionary for the sentence
				sentences.append({
					'text': text,
					'after_clean_text': after_clean_text,
					'hypernyms': hypernyms,
					'score': score
				})

				# We increase the counter
				count += 1

	# We create a new file for each hash tag file that we consulted.
	with open('Results/' + file + '.json', 'w') as outfile:
		# We finally dump the tweets + the overall_score in a json file.
		json.dump(sentences, outfile, indent=2)

	# End of the program's execution
	print("Total lines = " + str(count) + " we're processed.")
	print("Score assignation has finished successfully!")


# Here is a list that contains the names of the txt files that contain the twitter data
files_list = ['tweets_climatechange_06-03-2020_test', 'tweets_fridaysforfuture_09-03-2020_test',
              'tweets_savetheplanet_09-03-2020_test']
assign_scores(files_list)
