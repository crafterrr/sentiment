import re
import tweepy
from tweepy import OAuthHandler
from nltk.corpus import stopwords
from nltk import bigrams
import string
from collections import Counter
import operator
from Parse_tweet import *
from Building_charts import build_most_followed_table, build_sentiment_chart
import configparser


class TwitterClient(object):
    def __init__(self):
        # keys and tokens from the Twitter Dev Console
        config = configparser.ConfigParser()
        config.read('config.ini')
        config = config['MAIN']
        consumer_key = config['consumer_key']
        consumer_secret = config['consumer_secret']
        access_token = config['access_token']
        access_token_secret = config['access_token_secret']

        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def get_tweets(self, tweets_lang, query, count,
                   params):
        # query - keyword, count - tweet count
        # params - required fields
        # Main function to fetch tweets
        # empty list to store tweets
        tweets = []
        sinceid = None
        tweet_count = 0
        max_id = -1

        while tweet_count < count:
            try:
                if max_id <= 0:
                    if not sinceid:
                        fetched_tweets = self.api.search(q=query, count=count, lang=tweets_lang)
                    else:
                        fetched_tweets = self.api.search(q=query, count=count, lang=tweets_lang, since_id=sinceid)
                else:
                    if not sinceid:
                        fetched_tweets = self.api.search(q=query, count=count, lang=tweets_lang, max_id=str(max_id - 1))
                    else:
                        fetched_tweets = self.api.search(q=query, count=count, lang=tweets_lang, since_id=sinceid,
                                                         max_id=str(max_id - 1))
                if not fetched_tweets:
                    print('No more tweets found')
                    break

                good_tweets = 0
                # parsing tweets one by one
                for tweet in fetched_tweets:
                    # empty dictionary to store required params of a tweet
                    parsed_tweet = {}
                    try:
                        tweet.retweeted_status.user.id_str
                    except:
                        # saving text of tweet
                        '''parsed_tweet['text'] = [term for term in self.preprocess(tweet.text, lowercase=False) if
                                                    term not in stop]'''
                        parsed_tweet['text'] = tweet.text
                        if 'created_at' in params:
                            parsed_tweet['created_at'] = tweet.created_at
                        if 'retweet_count' in params:
                            parsed_tweet['retweet_count'] = tweet.retweet_count
                        parsed_tweet['user'] = tweet.user.screen_name
                        parsed_tweet['user_link'] = 'https://twitter.com/{user}'.format(user=parsed_tweet['user'])
                        parsed_tweet['followers'] = tweet.user.followers_count
                        parsed_tweet['tweet_url'] = 'https://twitter.com/{user}/status/{t_url}'.format(
                            t_url=tweet.id_str,
                            user=parsed_tweet['user'])
                        good_tweets += 1
                        tweets.append(parsed_tweet)
                tweet_count += good_tweets
                max_id = fetched_tweets[-1].id

            except tweepy.TweepError as e:
                # exit if any error
                print("some error: " + str(e))
                break

        # return tweets
        print('we got ', len(tweets), ' tweets')
        return tweets


def get_data(query, count=100, params=('text', 'created_at', 'retweet_count'), tweets_lang='en'):
    print(query)
    # creating object of TwitterClient Class
    api = TwitterClient()
    # calling function to get tweets
    tweets = api.get_tweets(query=query, count=count, params=params, tweets_lang=tweets_lang)

    return tweets
