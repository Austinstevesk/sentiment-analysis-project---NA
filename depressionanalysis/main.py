#!/usr/bin/env python
# coding: utf-8

# In[3]:


# This is Main function.
# Extracting streaming data from Twitter, pre-processing, and loading into MySQL

import credentials # Import api/access_token keys from credentials.py
import settings # Import related setting constants from pogdb.py 

import re
import tweepy
from textblob import TextBlob


# In[4]:


# Import api/access_token keys from credentials.py
import credentials
auth  = tweepy.OAuthHandler(credentials.API_KEY,                             credentials.API_SECRET_KEY)
auth.set_access_token(credentials.ACCESS_TOKEN,                        credentials.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


# In[5]:


#The fuctions are used to clean the tweets
def clean_tweet(self, tweet): 
    ''' 
    Use sumple regex statemnents to clean tweet text by removing links and special characters
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])                                 |(\w+:\/\/\S+)", " ", tweet).split()) 
def deEmojify(text):
    '''
    Strip all non-ASCII characters to remove emoji characters
    '''
    if text:
        return text.encode('ascii', 'ignore').decode('ascii')
    else:
        return None


# In[11]:


#This connnects to the database, checks if a table {"Tablename"} exits, if not creates one and closes the connection
import os
import psycopg2

dbconn = psycopg2.connect("host=ec2-52-207-25-133.compute-1.amazonaws.com dbname=d8e9au4m77k9b1 user=twvlbubsgabvpj password=53cf31e1928ac9f0ec3ec5554a92bfa96ddb693b7bb3b31df2bbf3784cc66f6a")
if dbconn:
    print("Connected")
    '''
    Check if this table exits. If not, then create a new one.
    '''
    mycursor = dbconn.cursor()
    """mycursor.execute(
    SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = '{0}'.format(settings.TABLE_NAME))
    print("table exists")"""
    mycursor.execute("select * from information_schema.tables where table_name=%s", ('nairobitweets',))
    if bool(mycursor.rowcount) == False:
    
        mycursor.execute("CREATE TABLE {} ({})".format(settings.TABLE_NAME, settings.TABLE_ATTRIBUTES))
        print("Table does not exist so it has been created")
        dbconn.commit()
        mycursor.close()
    else:
        print("Table already exists.")
        dbconn.commit()
        mycursor.close()
else:
    print('Not connected')


# In[12]:


#creating a listener to watch for our data
#has two functions
#on_status it to check for tweets
#on_error is to stop tweet checking incase a limit is reached
class MyStreamListener(tweepy.StreamListener):
    '''
    Tweets are known as “status updates”. So the Status class in tweepy has properties describing the tweet.
    https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object.html
    '''
    
    def on_status(self, status):
        '''
        Extract info from tweets
        '''
        
        if status.retweeted:
            # Avoid retweeted info, and only original tweets will be received
            return True
        # Extract attributes from each tweet
        id_str = status.id_str
        created_at = status.created_at
        text = deEmojify(status.text)    # Pre-processing the text  
        #sentiment = TextBlob(text).sentiment
        #polarity = sentiment.polarity
        #subjectivity = sentiment.subjectivity
        
        #user_created_at = status.user.created_at
        user_location = deEmojify(status.user.location)
        #user_description = deEmojify(status.user.description)
        #user_followers_count =status.user.followers_count
        longitude = None
        latitude = None
        if status.coordinates:
            longitude = status.coordinates['coordinates'][0]
            latitude = status.coordinates['coordinates'][1]
            print(longitude)
            print(latitude)
        retweet_count = status.retweet_count
        favorite_count = status.favorite_count
        
        print(status.text)
        print("Long: {}, Lati: {}".format(longitude, latitude))
        
        # Store all data in MySQL
        if dbconn:
            dbcursor = dbconn.cursor()
            sql = "INSERT INTO {} (id_str,created_at,text,                user_location,                longitude,                latitude, retweet_count, favorite_count) VALUES                 (%s, %s, %s, %s, %s, %s, %s, %s)".format(settings.TABLE_NAME)
            val = (id_str, created_at, text,                  user_location,longitude, latitude, retweet_count, favorite_count)
            dbcursor.execute(sql, val)
            dbconn.commit()
    
    def on_error(self, status_code):
        '''
        Since Twitter API has rate limits, stop scraping data as it exceed to the thresold.
        '''
        if status_code == 420:
            # return False to disconnect the stream
            return False


# In[13]:


#This calls the class myStreamListener thereby witing into the database
'''places = api.search(query="Nairobi", granularity="city")
place_id = places[0].id
public_tweets = api.search(q="place:%s" %place_id)
'''
GEOBOX_WORLD = [-180,-90,180,90]
GEOBOX_NAIROBI = [36.542329,-1.538666,37.186403,-1.052647]
while True:
    try:
        myStreamListener = MyStreamListener()
        myStream = tweepy.Stream(auth = api.auth, listener = myStreamListener)
        myStream.filter(languages=["en"], locations=GEOBOX_NAIROBI)
        dbconn.commit()
        # Close the postgres connection as it finished
        # However, this won't be reached as the stream listener won't stop automatically
        # Press STOP button to finish the process.
    except:
        dbconn = psycopg2.connect("host=ec2-52-207-25-133.compute-1.amazonaws.com dbname=d8e9au4m77k9b1 user=twvlbubsgabvpj password=53cf31e1928ac9f0ec3ec5554a92bfa96ddb693b7bb3b31df2bbf3784cc66f6a")
        myStreamListener = MyStreamListener()
        myStream = tweepy.Stream(auth = api.auth, listener = myStreamListener)
        myStream.filter(languages=["en"], locations=GEOBOX_NAIROBI)
        dbconn.commit()
    


# In[ ]:





# In[ ]:


#Fetch data from database


# In[ ]:





# In[4]:


#Connecting to the database and getting all the data in the database with a sleep time of 1 minute
import psycopg2 as pg
import pandas.io.sql as psql
import time
import pandas as pd
def getdata():
    connection = pg.connect("host=ec2-52-207-25-133.compute-1.amazonaws.com dbname=d8e9au4m77k9b1 user=twvlbubsgabvpj password=53cf31e1928ac9f0ec3ec5554a92bfa96ddb693b7bb3b31df2bbf3784cc66f6a")
    dataframe = psql.read_sql('SELECT * FROM nairobitweets', connection)
    dataframe.count
    print(dataframe)
    time.sleep(60)

while True:
    getdata()


# In[ ]:





# In[ ]:




