from sklearn.externals import joblib
import gensim
from gensim.models.keyedvectors import KeyedVectors
import plotly.express as px
import preprocessing_for_model
import numpy as np
import pandas as pd
import datetime
import nltk

import settings
import database_connection

while True:
    #setting time interval from which to fetch the tweets from db
    time_now = datetime.datetime.utcnow()
    time_10mins_before = datetime.timedelta(hours=0,minutes=10)
    print(time_10mins_before)
    time_interval = time_now - time_10mins_before
    print(time_interval)
    #fetching tweets from db
    query = "SELECT text, created_at FROM {} WHERE created_at >= '{}'".format(settings.TABLE_NAME, time_interval)
    df = pd.read_sql(query,database_connection.dbconn)
    print(df)

    #loading our word vectors
    word_vectors = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True, limit=20000)
    word_vectors.init_sims(replace=True)

    df['text'] = df['text'].astype(str)
    nltk.download('punkt')
    data_tokenized = df.apply(lambda r: preprocessing_for_model.w2v_tokenize_text(r['text']), axis=1).values
    data_averaged = preprocessing_for_model.word_averaging_list(word_vectors,data_tokenized)

    # Load the model from the file 
    depression_analyzer = joblib.load('testfile.sav')  
    
    # Use the loaded model to make predictions 
    df.text=df.text.astype(str)
    df['status'] = depression_analyzer.predict(data_averaged) 
    print(df.head())

    #plotting our bar_chart
    fig = px.bar(df, x="status")
    fig.show()