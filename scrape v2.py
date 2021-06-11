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

df = pd.DataFrame()
df['Post'] = ""
df['Date'] = ""
new_posts = reddit.subreddit('wallstreetbets').new(limit=10000)
for post in new_posts:
    appendDF = pd.DataFrame({"Post":[post.title] ,
                              "Date":[datetime.utcfromtimestamp(post.created).strftime('%Y-%m-%d %H:%M:%S')]       })
    df = df.append(appendDF , ignore_index = True)



df.to_csv('output.csv', index = False) 
print("done")








