from keras.layers.recurrent import LSTM
from keras.layers.core import Dropout, Dense, Activation
from keras.layers.embeddings import Embedding
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential, load_model
from keras import optimizers


class Neural_net:
    # Need to pass "load" or "embeddings" argument
    # if "load" is passed, other ones will be ignored
    def __init__(self, embeddings=None, n_layers=2, n_words=300,
                 dropout=0.5, load=None, *args):
        self.n_words = n_words
        if load:
            self.model = load_model(load)
            return
        self.model = Sequential()
        self.model.add(Embedding(input_dim=embeddings.shape[0],
                                 output_dim=embeddings.shape[1],
                                 weights=[embeddings]))
        self.model.add(LSTM(64, return_sequences=True))
        for i in range(n_layers - 2):
            self.model.add(LSTM(64, return_sequences=True))
        self.model.add(LSTM(64))
        self.model.add(Dropout(0.7))
        self.model.add(Dense(1))
        self.model.add(Activation('sigmoid'))
        print('Compilation started')
        self.model.compile(optimizer='adam',
                           loss='binary_crossentropy',
                           metrics=['binary_accuracy'])

    # Sentences must be encoded by ids to use this method
    def train(self, examples, labels):
        examples = self.__pad(examples)
        print('Training started')
        self.model.fit(examples, labels, verbose=1, nb_epoch=1)

    # Sentences must be encoded by ids to use this method
    def predict(self, examples):
        return self.model.predict(examples)

    def save(self, fname='LSTM.nn'):
        self.model.save(fname)

    def __pad(self, examples):
        examples = pad_sequences(examples, maxlen=self.n_words)
        return examples
