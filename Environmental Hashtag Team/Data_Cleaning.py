# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 19:30:14 2020
This code reads files containing twitter data and processes it to make it 
suitable for the word embedding function.

It converts emojis and emoticons into words, removes stop words and punctuation
and also stems the words.

@Chhandosee Bhattacharya: USER
"""

import emoji
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

import re

# This function cleans the data and makes it ready for Word Embedding
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

#Program starts here
#f = open('emoji.txt',encoding="utf8")
# We read the lines of the txt file.
#lines = f.readlines()
