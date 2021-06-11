import praw
from psaw import PushshiftAPI
import pandas as pd 
import time
from datetime import datetime
from datetime import datetime, timedelta
import numpy as np

id_ = 
secret = 
user = 


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


df = pd.DataFrame()
df['Post'] = ""

subreddit = "wallstreetbets"
validSubmissions = submissionsWithin24hours(subreddit)
for submission in validSubmissions:
    appendDF = pd.DataFrame({"Post":[submission]})
    df = df.append(appendDF , ignore_index = True)


df.to_csv('output.csv', index = False) 
print("done")









