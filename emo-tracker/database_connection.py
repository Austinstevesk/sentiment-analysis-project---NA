# Import api/access_token keys from credentials.py
import credentials
import tweepy
import os
import psycopg2
# Import related setting constants from settings.py
import settings 



#connecting to our database 
dbconn = psycopg2.connect("host=ec2-54-234-44-238.compute-1.amazonaws.com dbname=d5bo69edan88bi user=irdlmscnuoaofn password=861c0d9b502516c4ad6f4cf8aba2e851aed06c95b58f837a62c80af53ea062ea")
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

