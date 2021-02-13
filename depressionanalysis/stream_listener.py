import credentials

import tweepy
import psycopg2


import stream_listener_class
import database_connection

#setting up our api_keys
auth  = tweepy.OAuthHandler(credentials.API_KEY,credentials.API_SECRET_KEY)
auth.set_access_token(credentials.ACCESS_TOKEN,credentials.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

#This calls the class myStreamListener thereby witing into the database
GEOBOX_WORLD = [-180,-90,180,90]
GEOBOX_NAIROBI = [36.542329,-1.538666,37.186403,-1.052647]
while True:
    try:
        myStreamListener = stream_listener_class.MyStreamListener()
        myStream = tweepy.Stream(auth = api.auth, listener = myStreamListener)
        myStream.filter(languages=["en"], locations=GEOBOX_NAIROBI)
        database_connection.dbconn.commit()
        # Close the postgres connection as it finished
        # However, this won't be reached as the stream listener won't stop automatically
        # Press STOP button to finish the process.
    except:
        database_connection.dbconn = psycopg2.connect("host=ec2-52-207-25-133.compute-1.amazonaws.com dbname=d8e9au4m77k9b1 user=twvlbubsgabvpj password=53cf31e1928ac9f0ec3ec5554a92bfa96ddb693b7bb3b31df2bbf3784cc66f6a")
        myStreamListener = stream_listener_class.MyStreamListener()
        myStream = tweepy.Stream(auth = api.auth, listener = myStreamListener)
        myStream.filter(languages=["en"], locations=GEOBOX_NAIROBI)
        dbconn.commit()