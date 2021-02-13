import credentials
from datetime import datetime
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
        database_connection.dbconn = psycopg2.connect("host=ec2-54-234-44-238.compute-1.amazonaws.com dbname=d5bo69edan88bi user=irdlmscnuoaofn password=861c0d9b502516c4ad6f4cf8aba2e851aed06c95b58f837a62c80af53ea062ea")
        database_connection.dbconn = psycopg2.connect("host=ec2-3-222-150-253.compute-1.amazonaws.com dbname=d7r8l2rc7t54dg user=xsqferczoqicdo password=7d0958b2e4a979e088c6d39fb5e0b9d0ecf36681ddb312f3700519b3f088b990")

        

        myStreamListener = stream_listener_class.MyStreamListener()
        myStream = tweepy.Stream(auth = api.auth, listener = myStreamListener)
        myStream.filter(languages=["en"], locations=GEOBOX_NAIROBI)
        dbconn.commit()




