# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 16:08:44 2021

@author: Calven, Xun Yang
"""

import praw
from psaw import PushshiftAPI
import pandas as pd 
import time
from datetime import datetime
from datetime import datetime, timedelta
import numpy as np
import requests
from bs4 import BeautifulSoup
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from nltk.corpus import stopwords
import nltk
import matplotlib.pyplot as plt
import os

id_ = 
secret = 
user = 'WebScraping'

def comp_score(text):
   return analyser.polarity_scores(text)["compound"]   

reddit = praw.Reddit(client_id=id_, client_secret=secret, user_agent=user )


def submissionsWithin24hours(subreddit):
    subreddit = reddit.subreddit(subreddit)

    submissionsLast24 = []
    for submission in subreddit.new(limit=10000): 
        utcPostTime = submission.created
        submissionDate = datetime.utcfromtimestamp(utcPostTime)
        submissionDateTuple = submissionDate.timetuple()

        currentTime = datetime.utcnow()

        #How long ago it was posted.
        submissionDelta = currentTime - submissionDate

        title = submission.title
        link = 'www.reddit.com' + submission.permalink
        submissionDelta = str(submissionDelta)

        if 'day' not in submissionDelta:
            submissionsLast24.append(title)

    return submissionsLast24

directory = os.getcwd()
stockCode_df = pd.read_csv(directory+r'\data\All_Listed_Stock.csv')

wsb_df = pd.DataFrame()
wsb_df['Post'] = ""
wsb_df['Tick'] = ""

subreddit = "wallstreetbets"
validSubmissions = submissionsWithin24hours(subreddit)
for submission in validSubmissions:
   ticker = ""
   for j in range (len(stockCode_df)):
        tempList = submission.replace('$', '').split()
      stockcode = stockCode_df['Code'].iloc[[j]].to_string(index=False).strip()
      if any(word == stockcode for word in tempList ):
         ticker += stockcode
         ticker += ","
    appendDF = pd.DataFrame({"Post":[submission],
                             "Tick":[ticker]
                             })
    wsb_df = wsb_df.append(appendDF , ignore_index = True)

print("Outputing to csv...")
#wsb_df.to_csv('output.csv', index = False) 
print("Output to csv completed.")

#Vader Sentiment Analysis

# Add a new feature vader_score
analyser = SentimentIntensityAnalyzer()
wsb_df["vader_score"] = wsb_df["Post"].apply(comp_score)

#Data Understanding
print("There are {} observations and {} features in this dataset. \n".format(wsb_df.shape[0],wsb_df.shape[1]))
text = ' '.join(wsb_df.Post)
print ("There are {} words in the title on r/wsbets.".format(len(text)))


# Create stopword list
stop_words = set(STOPWORDS)
stop_words.update(nltk.corpus.stopwords.words('english'))

    
wordcloud = WordCloud(stopwords=stop_words, background_color="yellow", max_words = 40).generate(text)
plt.figure(figsize=(10,6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()
