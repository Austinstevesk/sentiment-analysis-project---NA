# -*- coding: utf-8 -*-

#This is the main file
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State
import os
import plotly
import plotly.graph_objs as go

import joblib
import plotly.express as px
import preprocessing_for_model
import pandas as pd
import datetime
import nltk
import sklearn
import psycopg2
import subprocess

import settings
import database_connection


# styling for the dash app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# download nltk dependencies
nltk.download('punkt')



app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])
colors = {
    'background': '#111111',
    'background2': '#FF0',
    'text': '#7FDBFF'
}

# global color setting
app_color = {
    "graph_bg": "rgb(221, 236, 255)",
    "graph_line": "rgb(8, 70, 151)",
    "graph_font": "rgb(2, 29, 65)"
}

# colors for plots
chart_colors = [
    '#664DFF',
    '#893BFF',
    '#3CC5E8',
    '#2C93E8',
    '#0BEBDD',
    '#0073FF',
    '#00BDFF',
    '#A5E82C',
    '#FFBD42',
    '#FFCA30'
]

app.layout = html.Div(children=[
    # the dash application layout 
    html.Div(
        [
            dcc.Interval(
                id='query_update',
                interval=int(5000),
                n_intervals=0,

            ),
            html.Div(
                #[html.H3("Mental Health", className='graph_title')]
            ),
            dcc.Graph(
                id='example-graph',
                animate=False,
                figure=go.Figure(
                    layout=go.Layout(
                        plot_bgcolor=app_color["graph_bg"],
                        paper_bgcolor=app_color["graph_bg"],
                    )
                ),
            ),

        ],
        className='graph__container first'
    )

])


# callback for the data processing
@app.callback(
    Output('example-graph', 'figure'),
    [Input('query_update', 'n_intervals')])
def update_graph_bar(n_intervals):
    # setting time interval from which to fetch the tweets from db
    time_now = datetime.datetime.utcnow()
    time_10mins_before = datetime.timedelta(hours=0, minutes=10)
    time_interval = time_now - time_10mins_before

    # fetching tweets from db
    time_now = datetime.datetime.utcnow()

    time_1day_before = datetime.timedelta(hours=1, minutes=0)
    # print(time_10mins_before)
    day_interval = time_now - time_1day_before
    print(".......")
    print(day_interval)
    print("......")

    # fetching tweets from db
    # added the time interval here
    # dt_string = now.strftime("%H:%M")
    del_time = "16:56"

    def deletedata():
        query = "DELETE FROM {} WHERE created_at <= '{}'".format(
            settings.TABLE_NAME, day_interval)
        print(query)
        conndb = database_connection.dbconn
        delcursor = conndb.cursor()
        delcursor.execute(query)
        conndb.commit()
        delcursor.close()

    deletedata()
    # added the time interval here
    query = "SELECT id_str, text, created_at, polarity,user_location FROM {} WHERE created_at >= '{}'".format(
        settings.TABLE_NAME, time_interval)
    df = pd.read_sql(query, database_connection.dbconn)

    df['text'] = df['text'].astype(str)
    df['clean_text'] = df['text'].apply(preprocessing_for_model.clean_dataset)
    # preprocessing the test data to make it suitable for the model
    '''   # Defining the basic parameters of the Neural Network
    maximum_words = 6000  # maximum words used in the corpus
    maximum_sequence_length = 280  # based on max. length of a single tweet
    embedding_dimension = 100  # dimensions of the embeddings used
    # initializing and tokenizing the provided words
    tokenizer = Tokenizer(num_words=maximum_words, filters='!"#$%&()*+,-./:;<=>?@[\]^_`{|}~', lower=True)
    word_index = tokenizer.word_index
    tokenizer.fit_on_texts(df['clean_text'].values)
    test_word_index = tokenizer.word_index

    test_data = tokenizer.texts_to_sequences(df['clean_text'].values)'''
    df['clean_text'] = df['text'].apply(preprocessing_for_model.clean_dataset)
    # Load the model from the file
    depression_analyzer = joblib.load('logreg_model.sav')

    # Use the loaded model to make predictions
    df.text = df.text.astype(str)
    predictions = depression_analyzer.predict(df['clean_text'])
    df['status'] = predictions
    # get the x and y values
    # setting the X and Y values
    realtime = datetime.datetime.utcnow()
    realtime_3hrs_after = datetime.timedelta(hours=3, minutes=0)
    heroku_time = realtime + realtime_3hrs_after
    X1 = datetime.datetime.now().strftime('%D, %H+3:%M:%S')
    X = heroku_time.strftime('%D, %H:%M:%S')
    print(X)
    Y1 = (df['status'] == 'Anger').sum()
    Y2 = (df['status'] == 'joy').sum()
    Y3 = (((df['status'] == 'Anger').sum())/(len(df.index)))*100
    Y4 = (((df['status'] == 'joy').sum())/(len(df.index)))*100
    
    return {
        'data': [
            {'x': [X], 'y': [Y3], 'type': 'bar', 'name': 'Unhappy (%)'},
            {'x': [X], 'y': [Y4], 'type': 'bar', 'name': 'Happy (%)'},
        ],
        'layout': {
            'title': 'Emotion distribution as per twitter sentiment analysis',
            # 'plot_bgcolor': colors['background'],
            # 'paper_bgcolor': colors['background']
        }
    }



if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run_server(debug=True, host='0.0.0.0', port=port)
