from word2vec import Vectorizer
from lstm import Neural_net
import pandas as pd
import numpy as np
from keras.models import Sequential, load_model
from keras.layers.recurrent import LSTM
from keras.layers.core import Dropout, Dense, Activation
from keras.layers.embeddings import Embedding
from keras import optimizers
from keras.preprocessing.sequence import pad_sequences
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score

def foo_model():
    vec = Vectorizer(load='w2v.vec')
    embeddings = vec.get_embeddings()
    model = Sequential()
    model.add(Embedding(input_dim=embeddings.shape[0], 
        output_dim=embeddings.shape[1], weights=[embeddings]))
    model.add(LSTM(64, return_sequences=True))
    model.add(LSTM(64))
    model.add(Dropout(0.8))
    model.add(Dense(1))
    model.add(Activation('sigmoid'))
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

df = pd.read_csv('positive.csv', sep=';', quotechar='"', usecols=[3,], header=None)
df['label'] = '1'

df2 = pd.read_csv('negative.csv', sep=';', quotechar='"', usecols=[3,], header=None)
df2['label'] = '0'

df = pd.merge(df, df2, how='outer')
df = df.dropna()

model = Vectorizer(load='w2v.vec')
# print('2')
labels = list(df['label'])
df = model.examples_to_id(list(df[3]))
df = pad_sequences(df, maxlen=300)
skf = StratifiedKFold(4)

print('PRESCORE')
classifier = KerasClassifier(build_fn=foo_model)
scores = cross_val_score(classifier, df, labels, cv=skf, 
    fit_params={'verbose':1, 'epochs':1}, n_jobs=-1, verbose=1)
print(scores)
f = open('cv_data.txt', 'w')
f.write(str(scores))

# df, labels = model.examples_to_vec(df, use_col=3)
# embeddings = model.get_embeddings()
# print('5')

# nn = Neural_net(embeddings)
# print('6')
# nn.train(df, labels)
# print('7')
# nn = Neural_net(load='1epad.nn')