    # -*- coding: utf-8 -*-
    """
    Created on Sun Apr 26 00:05:22 2020
    
    @author: Rucha Kulkarni
    """
    '''
    This code is about the implementation of the vader package to calculate the score for individual review and in overall
    Pcakge:    nltk:    python platform to deal with the natural language
               numpy:   library for the multi dimensional array with high level math functions
               pandas:  data manipulation and analysis
               vader:   A method/tool used to calculate the sentiment score specifically of social media
    Output:    A csv file with the sentiment score. 
    '''
    
    import nltk
    import numpy as np
    nltk.downloader.download('vader_lexicon')
    import re
    import pandas as pd
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    
    
    sid = SentimentIntensityAnalyzer()
    df = pd.read_csv('reviews.csv',delimiter=',', encoding="utf-8-sig")
    print(df.head())
    print(df['rating'].value_counts())
    
    dict = sid.polarity_scores(df.iloc[0]['reviewcontent'])  # prints analysis for first review
    print(dict)
    df['scores'] = ''    # calculates the polarity(positive,negative,neutral)
    df['scores'] = df['reviewcontent'].apply(lambda review:sid.polarity_scores(review))
    df.head()
    
    df['compound'] = ''
    df['compound'] = df['scores'].apply(lambda d:d['compound'])
    df.head()
    
    df['overall_score'] = ''   #for compound score
    df['overall_score'] = df['compound'].apply(lambda score: 'pos' if score >=0 else ('neg' if score <=-0.5 else 'neu'))
    
    def label_rating(df):   #function to label the rating column
         labels = []
         for row in range(df.shape[0]):
    
             if df['rating'][row]  <30:
               labels.append('neg')
            elif df['rating'][row] == 30:
                 labels.append('neu')
            elif df['rating'][row] >30:
                 labels.append('pos')
         return labels
    df['labels'] = label_rating(df)
    
    df.to_csv('Scores_file.csv', index= False)
    
    
    
    
