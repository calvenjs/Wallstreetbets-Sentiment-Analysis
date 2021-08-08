# WSB Sentiment Analysis
## Overview
Utilizing Python and Reddit PRAW API to scrape r/wallstreetbets over a 24h period, and perform sentiment analysis.
Overall, this project focuses on getting tickers that are most mentioned and speculated in the subreddit, the stocks' sentiments will complement the results.

On top of vader sentiment, the analysis uses a self-defined metric on derive the sentiment score on each ticker mentioned. It contains a list of positive words commonly used on tickers that the author has high conviction on e.g. moon, yolo, squeeze while a list of negative words e.g. mistake, out.

## Usage
1. Download the repository
2. Open the main.py file and edit the id and secret.
3. Run the script

## Output
1. Dataset

![image](https://user-images.githubusercontent.com/23024496/127808913-0dc06314-e942-446b-b37b-8ffdbc6e592e.png)

2. Frequency Table 

![image](https://user-images.githubusercontent.com/23024496/127806940-0ca27d37-62c6-4668-9e37-10986098e294.png)
    
