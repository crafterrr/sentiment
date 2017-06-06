from Parse_tweet import *
from plotly.offline import plot
import plotly.graph_objs as go
import plotly.plotly as py
import plotly.figure_factory as ff


def build_words_freq(freq_words):
    labels, freq = zip(*freq_words)
    data = [go.Bar(x=[label for label in labels],
                   y=[fr for fr in freq])]
    layout = dict(title='20 most common words',
                  yaxis=dict(title='frequency'),
                  xaxis=dict(title='words')
                  )
    fig = dict(data=data, layout=layout)
    return plot(fig, include_plotlyjs=False, output_type="div")


def build_time_freq(tweets_time):
    times, freq = zip(*sorted(tweets_time))
    data = [go.Scatter(x=[t for t in times],
                       y=[fr for fr in freq], mode='lines+markers')]
    layout = dict(title='Timeline',
                  yaxis=dict(title='number of tweets'),
                  )
    fig = dict(data=data, layout=layout)
    return plot(fig, include_plotlyjs=False, output_type="div")


def build_most_followed_table(most_followed_users):
    data_matrix = [['followers', 'link', 'tweet']]
    for user in most_followed_users:
        data_matrix.append([user[0][0], '<a href="https://twitter.com/{u}">{u}</a>'.format(u=user[0][1]),
                            '<a href="{t}">{t}</a>'.format(t=user[1])])
    table = ff.create_table(data_matrix)
    table.layout.width = 1400
    return plot(table, include_plotlyjs=False, output_type="div")


def build_hashtags_table(popular_hash):
    data_matrix = [['Times mentioned', 'hashtag']]
    for hashtag in popular_hash:
        data_matrix.append([hashtag[1], hashtag[0]])
    table = ff.create_table(data_matrix)
    table.layout.width = 700
    return plot(table, include_plotlyjs=False, output_type="div")


# gets (positive, negative)
def build_sentiment_chart(sentiment):
    labels = ['Positive', 'Negative']
    values = [sentiment[0], sentiment[1]]
    colors = ['#98FB98', '#CD5C5C']

    trace = go.Pie(labels=labels, values=values, textfont=dict(size=20),
                   hoverinfo='label+percent', marker=dict(colors=colors,
                                                          line=dict(color='#000000', width=2)))

    return plot([trace], include_plotlyjs=False, output_type="div")
