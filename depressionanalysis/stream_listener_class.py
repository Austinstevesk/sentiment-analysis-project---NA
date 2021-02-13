import tweepy
import psycopg2
import database_connection
import settings
import preprocessing_for_db

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
        text = preprocessing_for_db.deEmojify(status.text)    # Pre-processing the text  
        user_location = preprocessing_for_db.deEmojify(status.user.location)
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
        if database_connection.dbconn:
            dbcursor = database_connection.dbconn.cursor()
            sql = "INSERT INTO {} (id_str,created_at,text,\
                user_location,\
                longitude,\
                latitude, retweet_count, favorite_count) VALUES \
                (%s, %s, %s, %s, %s, %s, %s, %s)".format(settings.TABLE_NAME)
            val = (id_str, created_at, text,\
                  user_location,longitude, latitude, retweet_count, favorite_count)
            dbcursor.execute(sql, val)
            database_connection.dbconn.commit()
    
    def on_error(self, status_code):
        '''
        Since Twitter API has rate limits, stop scraping data as it exceed to the thresold.
        '''
        if status_code == 420:
            # return False to disconnect the stream
            return False
