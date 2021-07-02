# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 16:08:44 2021

@author: Calven, Xun Yang
"""

import praw
from psaw import PushshiftAPI
import pandas as pd
pd.options.mode.chained_assignment = None
from datetime import timedelta
import datetime
import numpy as np
import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
import matplotlib.pyplot as plt
import re
import yfinance as yf


id_ =  
secret = 
user = 'WebScraping'

def comp_score(text):
   return analyser.polarity_scores(text)["compound"]   

reddit = praw.Reddit(client_id=id_, client_secret=secret, user_agent=user )


def submissionsWithin24hours(subreddit):
    subreddit = reddit.subreddit(subreddit)

    submissionsLast24 = []
    selfText24 = []
    for submission in subreddit.new(limit=10000): 
        utcPostTime = submission.created
        submissionDate = datetime.datetime.utcfromtimestamp(utcPostTime)
        submissionDateTuple = submissionDate.timetuple()

        currentTime = datetime.datetime.utcnow()

        #How long ago it was posted.
        submissionDelta = currentTime - submissionDate

        title = submission.title
        link = 'www.reddit.com' + submission.permalink
        body = submission.selftext
        submissionDelta = str(submissionDelta)

        if 'day' not in submissionDelta:
            submissionsLast24.append(title)
            selfText24.append(body)

    return selfText24, submissionsLast24


wsb_df = pd.DataFrame()
wsb_df['Post'] = ""
wsb_df['Body'] = ""
wsb_df["Ticker"] = ""
wsb_df['Sentiment Score'] = 0
pd.set_option('display.max_columns', None)

subreddit = "wallstreetbets"
body, validSubmissions = submissionsWithin24hours(subreddit)
i = 0
for submission in validSubmissions:
    appendDF = pd.DataFrame({"Post":[submission],
                             "Body":[body[i]],
                             "Ticker":[""],
                             'Sentiment Score':[0]
                            })
    i+=1
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
# Word Cloud
wordcloud = WordCloud(stopwords=stop_words, background_color="yellow", max_words = 40).generate(text)
plt.figure(figsize=(10,6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

# Get tickers
tickers = set()
outlook_dict = {}
negative = ['put','down','sell','drop','fall','lose','bear','out','bad','mistake','useless']
positive = ['call','long','up','buy','bull','in','good','hold','hodl','love','yolo','all in','discount','moon','squeeze']
black_list= ['DD','APE','POOR','CEO','LAST','IT','IN','BUY','FED','USA','SEC','MY','PR','JUST','ALL','THIS','THE','LOOKS','LIKE','ART','HOMO','BET','FOMO','WSB','MOON','LAMBO','HF', 'LOL', 'I', 'SEE', 'BRRR','BRR','STOP', 'YOLO', 'TIL', 'EDIT', 'OTM', 'GOT', 'IPO', 'WTF', 'A', 'ATH','FUCK','BUT','UP','COVID']

dict_freq = pd.DataFrame()
dict_freq['Name'] = ""
dict_freq['Frequency'] = ""


for i in range(0, len(wsb_df)):
   temp = re.findall("(?:(?<=\A)|(?<=\s)|(?<=[$]))([A-Z]{1,5})(?=\s|$|[^a-zA-z])", wsb_df["Post"][i])
   tickerFound = ""
   for word in temp:
      for negword in negative:
         if negword in wsb_df["Post"][i].lower():
            wsb_df["Sentiment Score"][i] += -5
      for posword in positive:
         if posword in wsb_df["Post"][i].lower():
            wsb_df["Sentiment Score"][i] += 5

      if word in black_list:
         temp.remove(word)
         #print('Removing ' + word)
      else:
         ticker = word
         tickerObj = yf.Ticker(ticker)
         try:
            if tickerObj.info['symbol'] == ticker:
               #print("Matching ticker found for " + ticker)
               if ticker in dict_freq.Name.values:
                  dict_freq.loc[(dict_freq.Name == ticker), 'Frequency'] =  dict_freq.loc[(dict_freq.Name == ticker), 'Frequency'] + 1
               else:
                  dict_freq = dict_freq.append( pd.DataFrame({"Name" : [ticker], "Frequency" : [1]}))
               tickers.add(ticker)
               if tickerFound !=  "":
                  tickerFound += ","
               tickerFound += ticker
         except:
            #print("No such ticker for " + ticker)
            continue  
      wsb_df["Ticker"][i] = tickerFound
      


# Get stock Adjusted close
start = datetime.datetime.today()-datetime.timedelta(100)
end =  datetime.datetime.today()
cl_price = pd.DataFrame()

# Print Bar Chart(Frequency)
dict_freq = dict_freq[dict_freq.Frequency > 1]
ax = dict_freq.sort_values(by='Frequency', ascending =False).plot.bar(x="Name", y= "Frequency", rot=0)
ax.set_title("Frequency Table of WSB")
ax.set_xlabel("Stock Code")
ax.set_ylabel("Frequency")
plt.show()


for ticker in tickers:
    cl_price[ticker] = yf.download(ticker, start, end )["Adj Close"]
