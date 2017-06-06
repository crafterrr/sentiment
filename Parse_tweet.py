# coding=UTF-8
import re
import string
from nltk.corpus import stopwords
from collections import Counter
from nltk.stem.snowball import SnowballStemmer
import operator


def preprocess(s, lowercase=True):
    emoticons_str = r"""
        (?:
            [:=;] # Eyes
            [oO\-]? # Nose (optional)
            [D\)\]\(\]/\\OpP] # Mouth
        )"""

    regex_str = [
        emoticons_str,
        r'<[^>]+>',  # HTML tags
        r'(?:@[\w_]+)',  # @-mentions
        r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",  # hash-tags
        r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',  # URLs

        r'(?:(?:\d+,?)+(?:\.?\d+)?)',  # numbers
        r"(?:[a-z][a-z'\-_]+[a-z])",  # words with - and '
        r'(?:[\w_]+)',  # other words
        r'(?:\S)'  # anything else
    ]

    tokens_re = re.compile(r'(' + '|'.join(regex_str) + ')', re.VERBOSE | re.IGNORECASE)
    emoticon_re = re.compile(r'^' + emoticons_str + '$', re.VERBOSE | re.IGNORECASE)

    tokens = tokens_re.findall(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens


def parsing(tweet, lang='english'):
    punctuation = list(string.punctuation)
    stop = stopwords.words(lang) + punctuation + ['rt', 'via', 'RT', '…', '“', '”', '’', "'", '"', '`', '«', '»', 'amp',
                                                  '–']
    parsed_tweet = [term for term in preprocess(tweet, lowercase=True) if
                    term not in stop]
    return parsed_tweet


def remove_shit(word):
    return (not word.startswith(('#', '@', 'http', '&')) and not word.endswith('\n')) or (
        word.isdigit() and len(word) == 4 and not word.endswith('\n'))


def common_words(tweets):
    stemmer = SnowballStemmer("english")
    count_words = Counter()
    for tweet in tweets:
        words = [stemmer.stem(word) for word in parsing(tweet['text'], 'english') if remove_shit(word)]
        count_words.update(words)
    return count_words.most_common(20)


def tweets_timeline(tweets):
    count_timeline = Counter()
    timeline = [tweet['created_at'] for tweet in tweets]
    count_timeline.update(timeline)
    return count_timeline.most_common(100)


def popular_hashtags(tweets):
    count_hashtag = Counter()
    for tweet in tweets:
        hashtags = [word for word in parsing(tweet['text'], 'english') if word.startswith('#')]
        count_hashtag.update(hashtags)
    return count_hashtag.most_common(20)


# retweet frequency (number of retweets, tweet, tweet_link, user_link) for each
def retweet_freq(tweets):
    # all_tweets = [tweet for tweet in tweets]
    retweeted_tweets = []
    for tweet in sorted(tweets, key=operator.itemgetter('retweet_count'), reverse=True)[:20]:
        if tweet['retweet_count'] > 0:
            retweeted_tweets.append((tweet['retweet_count'], tweet['text'], tweet['tweet_url'], tweet['user_link']))
    return retweeted_tweets


# most followed users [(number of followers, user_link), list of user tweets]
def most_followed(tweets):
    users = []
    for tweet in tweets:
        if (tweet['followers'], tweet['user']) not in users:
            users.append((tweet['followers'], tweet['user']))
    users_tweets = []
    for user in sorted(users, reverse=True)[:20]:
        for tweet in sorted(tweets, key=operator.itemgetter('retweet_count'), reverse=True):
            if tweet['user'] == user[1]:
                users_tweets.append((user, tweet['tweet_url']))
                break
    return users_tweets
