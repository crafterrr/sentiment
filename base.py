from word2vec import Vectorizer
from lstm import NeuralNet
import pandas as pd
import numpy as np
from keras.preprocessing.sequence import pad_sequences


# Provides simple interface to use NeuralNet and Word2vec opportunities


class NeuralNetInterface:
    def __init__(self, n_words, neural_net='1epad', vectorizer='w2v'):
        self.n_words = n_words
        self.vec = Vectorizer(load='{}.vec'.format(vectorizer))
        self.nn = NeuralNet(load='{}.nn'.format(neural_net), n_words=n_words)

    # Sentences must be represented as strings
    def nn_train(self, sentences, labels):
        sentences = self.vec.examples_to_id(list(sentences))
        labels = list(labels)
        self.nn.train(sentences, labels)

    # Sentences must be represented as strings
    def nn_predict(self, sentences, disjoined=False):
        if disjoined:
            for i in range(0, len(sentences)):
                sentences[i] = ' '.join(sentences[i])
        sentences = self.vec.examples_to_id(list(sentences))
        # sentences = np.array(sentences)
        sentences = pad_sequences(sentences, maxlen=self.n_words)
        return self.nn.predict(sentences)

    # Does something about word similarity
    def word_similar(self, word):
        pass

    # ???
    def other_word_methods(self, word, *args):
        pass
