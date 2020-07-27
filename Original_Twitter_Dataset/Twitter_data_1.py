import os
import tweepy as tw
import pandas as pd
import datetime as dt
from twitterscraper import query_tweets

# Twitter API credentials
consumer_key= 'consumer_key'
consumer_secret= 'consumer_secret'
access_token= 'access_token'
access_token_secret= 'access_token_secret'

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

tweets = tw.Cursor(api.search, q='coronavirus', 
                       result_type='popular',lang='en',since='2020-03-01',tweet_mode='extended').items(200)
users_locs = [[tweet.user.id, 
               tweet.user.screen_name, 
               tweet.user.location,
               tweet.full_text, 
               tweet.entities['hashtags'], 
               tweet.favorite_count, 
               tweet.retweet_count,
               tweet.created_at] for tweet in tweets]

tweet_text = pd.DataFrame(data=users_locs, 
                 columns=['id','user', 'location', 'Tweet', 'Hashtags', 'likes', 'Retweets', 'Date'])

print(tweet_text.shape)

# Does not get all data so using Twitterscraper library

start_date = dt.date(2020,5,1)
end_date = dt.date(2020,7,15)
language = 'english'
delta = dt.timedelta(days=1)
file_append = 'Tweets'

while start_date <= end_date:

    print(start_date)
    list_of_tweets = query_tweets("#COVID2019 OR #COVID19 OR corona&virus", limit = 2000, begindate=start_date,enddate=start_date+delta,lang=language)
    #print(list_of_tweets[1].__dict__)
    covid_tweets = pd.DataFrame((t.__dict__ for t in list_of_tweets))
    filename = file_append + start_date.strftime("%d-%m-%Y")+'.csv'
    covid_tweets.to_csv(filename,index=False)
    start_date += delta
