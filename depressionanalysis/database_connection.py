# Import api/access_token keys from credentials.py
import credentials
import tweepy
import os
import psycopg2
# Import related setting constants from pogdb.py 
import settings 



#connecting to our database
dbconn = psycopg2.connect("host=ec2-52-207-25-133.compute-1.amazonaws.com dbname=d8e9au4m77k9b1 user=twvlbubsgabvpj password=53cf31e1928ac9f0ec3ec5554a92bfa96ddb693b7bb3b31df2bbf3784cc66f6a")

#checking whether our table exists,if not create a new one
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

