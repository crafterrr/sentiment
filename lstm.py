from keras.layers.recurrent import LSTM
from keras.layers.core import Dropout, Dense, Activation
from keras.layers.embeddings import Embedding
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential, load_model
from keras import optimizers
from keras.utils.np_utils import to_categorical
from keras import regularizers


class NeuralNet:
    # Need to pass "load" or "embeddings" argument
    # if "load" is passed, other ones will be ignored
    # "n_words" must be passed anyway for correct work
    def __init__(self, n_words, embeddings=None, n_layers=2,
                 dropout=0.5, load=None):
        self.n_words = n_words
        self.reg = 1
        if load:
            self.model = load_model(load)
            return
        self.model = Sequential()
        self.model.add(Embedding(input_dim=embeddings.shape[0],
                                 output_dim=embeddings.shape[1],
                                 weights=[embeddings]))
        for _ in range(n_layers - 2):
            self.model.add(LSTM(64, return_sequences=True))
        self.model.add(
            LSTM(64, return_sequences=True, go_backwards=True))  # Should activation='relu' be added to all LSTM's?
        self.model.add(LSTM(64, go_backwards=True))
        # self.model.add(LSTM(64))
        self.model.add(Dropout(dropout))
        self.model.add(Dense(1, kernel_regularizer=regularizers.l2(self.reg),
                             activity_regularizer=regularizers.l2(self.reg),
                             bias_regularizer=regularizers.l2(self.reg)))  # 1))
        self.model.add(Activation('softmax'))  # or sigmoid(?)
        print('Compilation started')
        self.model.compile(optimizer='RMSprop',
                           loss='binary_crossentropy',
                           metrics=['accuracy',
                                    'binary_accuracy',
                                    'categorical_accuracy',
                                    'sparse_categorical_accuracy'])

    # Sentences must be encoded by ids to use this method
    def train(self, examples, labels):
        examples = self.__pad(examples)
        print('Training started')
        # labels = to_categorical(labels, num_classes=2)
        self.model.fit(examples, labels, verbose=1, epochs=1)

    # Sentences must be encoded by ids to use this method
    def predict(self, examples):
        return self.model.predict(examples)

    def save(self, fname='LSTM.nn'):
        self.model.save(fname)

    def __pad(self, examples):
        examples = pad_sequences(examples, maxlen=self.n_words)
        return examples
