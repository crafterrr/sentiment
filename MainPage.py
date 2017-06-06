import json
from Building_charts import *
from Parse_tweet import common_words, tweets_timeline, most_followed, popular_hashtags
from bottle import run, post, get, template, request, route, redirect
from Get_tweets import get_data
from base import NeuralNetInterface

neural_net = NeuralNetInterface(neural_net='lstm_2layer', n_words=140)


@get('/')
@get('/query')
def get_query():
    return template('get_query.html')


@post('/post_query')
def fulfill():
    query = request.forms.getunicode('keyword')
    result = get_data(query)
    texts = []
    for i in result:
        texts.append(i['text'])
    prediction = neural_net.nn_predict(texts)
    if len(prediction) == 0:
        return 'Sorry, something went wrong when downloading tweets'
    prediction = sum(prediction) / len(prediction)
    prediction = prediction[0]
    return template('charts.html', words_freq=build_words_freq(common_words(result)),
                    most_followed=build_most_followed_table(most_followed(result)),
                    hashtags=build_hashtags_table(popular_hashtags(result)),
                    time_freq=build_time_freq(tweets_timeline(result)),
                    sentiment_ch=build_sentiment_chart((prediction, 1 - prediction)))


run(host='localhost', port=8080)
