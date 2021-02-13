#!/usr/bin/env python
# coding: utf-8

# In[1]:


import plotly.express as px
import psycopg2
import datetime


# In[ ]:


#connecting to db
dbconn = psycopg2.connect("host=ec2-52-207-25-133.compute-1.amazonaws.com dbname=d8e9au4m77k9b1 user=twvlbubsgabvpj password=53cf31e1928ac9f0ec3ec5554a92bfa96ddb693b7bb3b31df2bbf3784cc66f6a")

#setting time interval from which to fetch the tweets from db
time_now = datetime.datetime.utcnow()
time_10mins_before = datetime.timedelta(hours=0,minutes=10).strftime('%Y-%m-%d %H:%M:%S')
time_interval = time_now - time_10mins_before

#fetching tweets from db
query = "SELECT id_str, text, created_at, polarity,user_location FROM {} WHERE created_at >= '{}'".format(settings.TABLE_NAME, time_interval)
df = pd.read_sql(query, con=db_conn)


# In[3]:


#plottin our pie_chart
print(df.head())
fig = px.pie(df, values='tip', names='day')
fig.show()


# In[ ]:




