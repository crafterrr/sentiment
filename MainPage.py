import json
from Building_charts import *
from Parse_tweet import common_words, tweets_timeline, most_followed, popular_hashtags
from flask import request, Flask, render_template
from Get_tweets import get_data
from base import NeuralNetInterface

neural_net = NeuralNetInterface(neural_net='lstm_2layer', n_words=140)

app = Flask(__name__)

@app.route('/')
@app.route('/query')
def get_query():
    return render_template('get_query.html')


@app.route('/post_query', methods=['GET', 'POST'])
def fulfill():
    # query = request.forms.getunicode('keyword')
    query = request.form['keyword']
    result = get_data(query)

    texts = []
    for i in result:
        texts.append(i['text'])

    prediction = neural_net.nn_predict(texts)

    if len(prediction) == 0:
        return 'Sorry, something went wrong when downloading tweets'
    
    prediction = sum(prediction) / len(prediction)
    prediction = prediction[0]

    return render_template('charts.html', words_freq=build_words_freq(common_words(result)),
                    most_followed=build_most_followed_table(most_followed(result)),
                    hashtags=build_hashtags_table(popular_hashtags(result)),
                    time_freq=build_time_freq(tweets_timeline(result)),
                    sentiment_ch=build_sentiment_chart((prediction, 1 - prediction)))

if __name__ == '__main__':
    app.run(host='localhost', port=8080)
