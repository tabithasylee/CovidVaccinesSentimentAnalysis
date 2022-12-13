import PySimpleGUI as sg

from twarc import Twarc
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import keras
import numpy as np

from keras.preprocessing.text import Tokenizer
from keras_preprocessing.sequence import pad_sequences
from keras import regularizers

max_words = 5000 # max words in tweet
max_len = 300 # max length of tweet

# initialize tokenizer with max words in tweet
tokenizer = Tokenizer(num_words=max_words)
# Download the lexicon
nltk.download("vader_lexicon")

consumer_key = "zV9NpesB6qdytvyi3GDpREEhk"
consumer_secret = "uzECwlEqfz4Pj7fawkIvLwE81zrGOyhWpJ4cUJTQ6DF2MufVWs"
access_key = "1592302414182260736-0vavMgY6qmXEkHBkP9i8obLpG399nN"
access_secret = "6rypViyoG3G699ZslLvQApfVwEecwA4UxYAD9GNTkzy9E"
model = keras.models.load_model('model/sentiments_model.hdf5')

t = Twarc(consumer_key, consumer_secret, access_key, access_secret)

def hydrate_and_get_results(value):
    sent_analyzer = SentimentIntensityAnalyzer()
    
    tweet = t.tweet(value)
    if tweet:
        fields = [tweet['created_at'], tweet['full_text'], tweet['user']['followers_count'], tweet['user']['location'], tweet['retweet_count'], tweet['favorite_count'], tweet['entities']['hashtags']]
    else:
        return 0, 0, 0, 0, "", ""
    scores = sent_analyzer.polarity_scores(fields[1])
        
    # default polarity classification is neutral
    polarity = "neutral"
    
    # assign each of the polarity scores to variables
    negative = scores['neg']
    neutral = scores['neu']
    positive = scores['pos']
    overall = scores['compound']
    
    # re-assign polarity classification depending on compound value
    if overall >= 0.05:
        polarity = "positive"
    elif overall <= -0.05:
        polarity = "negative"
        
    # returns a tuple of polarity scores as well as the polarity classification
    return [negative, neutral, positive, overall, polarity, fields[1]]

sg.theme('DarkBlue11')   # Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Text('Tweet Analyzer')],
            [sg.Text('Enter a tweet ID'), sg.InputText()],
            [sg.Button('Ok'), sg.Button('Cancel')] ,
            [sg.Text("", key="tweet")]]

# Create the Window
window = sg.Window('Window Title', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    score = hydrate_and_get_results(values[0])
    text = []
    text.append(f"Text of the tweet: \n '{score[5]}'")
    text.append(f'Negative sentiment score: {score[0]}')
    text.append(f'Neutral sentiment score: {score[1]}')
    text.append(f'Positive sentiment score: {score[2]}')
    text.append(f'Overall sentiment score: {score[3]}')
    text.append(f'Polarity: {score[4]}')
        
    testing_sequences = tokenizer.texts_to_sequences([score[5]])
    testing_padded = pad_sequences(testing_sequences, maxlen=max_len)
    predictions = model.predict(testing_padded)
    y_classes = [np.argmax(y, axis=None, out=None) for y in predictions]
    dictionary = {
        0: "negative",
        1: "neutral",
        2: "positive"
    }
    prediction = [dictionary[x] for x in y_classes]
    text.append(f'Neural Network Prediction: {prediction[0]}')
    window["tweet"].update("\n".join(text))

window.close()
