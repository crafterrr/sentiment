from word2vec import Vectorizer
from lstm import Neural_net
import pandas as pd
import numpy as np

# Provides simple interface to use Neural_net and Word2vec opportunities


class Interface:
    def __init__(self, neural_net='1epad', vectorizer='w2v'):
        self.vec = Vectorizer(load='{}.vec'.format(vectorizer))
        self.nn = Neural_net(load='{}.nn'.format(neural_net))

    # Sentences must be represented as strings
    def nn_train(self, sentences, labels):
        sentences = self.vec.examples_to_id(list(sentences))
        labels = list(labels)
        self.nn.train(sentences, labels)

    # Sentences must be represented as strings
    def nn_predict(self, sentences):
        sentences = self.vec.examples_to_id(list(sentences))
        sentences = np.array(sentences)
        return self.nn.predict(sentences)

    # Does something about word similarity
    def word_similar(self, word):
        pass

    # ???
    def other_word_methods(self, word, *args):
        pass

interface = Interface()
