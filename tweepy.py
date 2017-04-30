import re
import tweepy
from tweepy import OAuthHandler
from nltk.corpus import stopwords
import string

class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''

    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        consumer_key = ''
        consumer_secret = ''
        access_token = ''
        access_token_secret = ''

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

    def preprocess(self, s, lowercase=False):

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

    def get_tweets(self, tweets_lang, query, count, params): #query - ключевое слово, count - кол-во сообщений, params - необходимые поля
        '''
        Main function to fetch tweets and parse them.
        '''
        punctuation = list(string.punctuation)
        stop = stopwords.words('russian') + punctuation + ['rt', 'via']+ ['«', '»']
        # empty list to store parsed tweets
        tweets = []
        sinceID = None
        tweetCount = 0
        max_id = -1


        while tweetCount < count:
            try:
                if max_id <= 0:
                    if not sinceID:
                        fetched_tweets = self.api.search(q=query, count=count, lang=tweets_lang)
                    else:
                        fetched_tweets = self.api.search(q=query, count=count, lang=tweets_lang, since_id=sinceID)
                else:
                    if not sinceID:
                        fetched_tweets = self.api.search(q=query, count=count, lang=tweets_lang, max_id=str(max_id-1))
                    else:
                        fetched_tweets = self.api.search(q=query, count=count, lang=tweets_lang, since_id=sinceID, max_id=str(max_id-1))
                if not fetched_tweets:
                    print('No more tweets found')
                    break

                # parsing tweets one by one
                for tweet in fetched_tweets:
                    # empty dictionary to store required params of a tweet
                    parsed_tweet = {}
                    if 'text' in params:
                        # saving text of tweet
                        # parsed_tweet['text'] = self.preprocess(tweet.text, lowercase=False)
                        parsed_tweet['text'] = [term for term in self.preprocess(tweet.text, lowercase=False) if
                                                term not in stop]
                    if 'created_at' in params:
                        parsed_tweet['created_at'] = tweet.created_at
                    if 'retweet_count' in params:
                        parsed_tweet['retweet_count'] = tweet.retweet_count
                    if 'favorite_count' in params:
                        parsed_tweet['favorite_count'] = tweet.favorite_count
                    parsed_tweet['user'] = tweet.user.id_str

                    # appending parsed tweet to tweets list
                    '''if tweet.retweet_count > 0:
                        # if tweet has retweets, ensure that it is appended only once
                        if parsed_tweet not in tweets:
                            tweets.append(parsed_tweet)
                    else:
                        tweets.append(parsed_tweet)'''
                    tweets.append(parsed_tweet)
                tweetCount += len(fetched_tweets)
                max_id = fetched_tweets[-1].id



            except tweepy.TweepError as e:
                # exit if any error
                print("some error: " + str(e))
                break


        # return parsed tweets
        return tweets



def get_data(query, count=100, params=['text'], tweet_lang='ru'):
    # creating object of TwitterClient Class
    api = TwitterClient()
    # calling function to get tweets
    tweets = api.get_tweets(query=query, count=count, params=params, tweets_lang=tweets_lang)
    # returns parsed tweets as a list of dictionaries for each tweet
    # ex {'text'=['Путин', 'войдёт', 'историю'], 'created_at': datetime.datetime(2017, 4, 23, 13, 14, 29), 'favorite_count': 0, 'retweet_count': 7}
    return tweets

