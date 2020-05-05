# -*- coding: utf-8 -*-
"""
Created on Fri May  1 23:21:59 2020

@author: Rucha Kulkarni
"""
'''
This code calculates the f1 score,accuracy and other measures for the labled data and the overall score columns

Packages:   sklearn:- library that features algo like random forest,KNN,Vector machines and supports NumPy and SciPy

Output:  classification report with the f1 score and Accuracy.
'''

import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score,classification_report,confusion_matrix,f1_score

df = pd.read_csv('Scores_file.csv',delimiter=',', encoding="utf-8-sig")
pd.set_option('.max_columns', 8)   
print(df.head())
encode = LabelEncoder()
features = df.iloc[:,:,].values

#Label encoding for the columns labels and overall_score
df['encoded_Label1'] = encode.fit_transform(df['labels'])
#df = pd.DataFrame(df)
df['encoded_Label2'] = encode.fit_transform(df['overall_score'])
#df = pd.DataFrame(df)
df.to_csv('final_file.csv',index=False)

df1 = pd.read_csv('final_file.csv',delimiter=',', encoding="utf-8-sig")


print(accuracy_score(df1['encoded_Label1'],df1['encoded_Label2']))

print(classification_report(df1['encoded_Label1'],df1['encoded_Label2']))

