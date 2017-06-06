from nltk.tokenize import wordpunct_tokenize
from gensim.models.word2vec import Word2Vec
import numpy as np
from Parse_tweet import parsing


# It'll be better to use Python list rather
# than Pandas dataframes (works significantly faster)


class Vectorizer:
    # Need to pass "load" or "sentences" argument, if "load" is passed,
    # other ones will be ignored
    def __init__(self, sentences=None, size=300,
                 alpha=0.025, iter=5, load=None):
        self.size = size
        if load:
            self.model = Word2Vec.load(load)
            return
        if do_tfrom:
            sentences = self.transform(sentences)
        self.model = Word2Vec(sentences, size=size, alpha=alpha, iter=iter)

    def train(self, sentences):
        self.model.train(sentences)

    def save(self, fname='w2v'):
        self.model.save('{}.vec'.format(fname))

    # Returns word vector for given word
    # (None or zeros vector if there is no such word in vocab)
    def vectorize(self, word, return_zeros=False):
        try:
            answer = self.model.wv[word]
        except:
            if return_zeros:
                return np.zeros(self.size)
            return None
        return answer

    # Gets list of sentences and returns them as wordlist with words
    # encoded with word vectors
    def examples_to_vec(self, examples):
        new_examples = []
        examples = self.transform(examples)
        for example in examples:
            sen = []
            for word in example:
                temp = self.vectorize(word)
                if temp is not None:
                    sen.append(temp)
            new_examples.append(sen)
        return new_examples

    # Gets list of sentences and returns them as wordlist with words
    # encoded with their ids
    def examples_to_id(self, examples):
        new_examples = []
        vocab = self.get_vocab()
        examples = self.transform(examples)
        for example in examples:
            sen = []
            for word in example:
                if word in vocab.keys():
                    sen.append(vocab[word])
            new_examples.append(sen)
        return new_examples

    # returns word vectors
    # (can be used as weights in neural net embedding layer)
    def get_embeddings(self):
        return self.model.wv.syn0

    # returns dictionary (format word:id or id:word if reverse=True)
    def get_vocab(self, reverse=False):
        if reverse:
            answer = dict([(id.index, word) for
                           word, id in self.model.wv.vocab.items()])
        else:
            answer = dict([(word, id.index) for
                           word, id in self.model.wv.vocab.items()])
        return answer

    # transforms sentence into list of words and symbols
    def transform(self, sentences):
        new_sent = [parsing(sent) for sent in sentences]
        return sentences
