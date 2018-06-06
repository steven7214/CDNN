#!/usr/bin/env python3

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LeakyReLU
from keras.layers import ELU
from sklearn.model_selection import StratifiedKFold
import numpy
import os

numpy.random.seed(7)

filename = os.path.join( os.getcwd(), '..', 'Data/CancerSEEK/Only Numbers (normal).csv' )
data = numpy.loadtxt(filename, delimiter=",")
#split data
input = data[:, 0:39]
output = data[:, 39]

#define 10-fold cross validation
kfold = StratifiedKFold(n_splits=10, shuffle=True, random_state = 7)
list = []
for train, test in kfold.split(input, output):
    #build model
    model = Sequential()
    model.add(Dense(40, input_dim=39, activation='tanh'))
    #model.add(ELU(alpha = 1.0))
    model.add(Dense(25, activation='tanh'))
    #model.add(ELU(alpha = 1.0))
    model.add(Dense(1, activation='sigmoid'))
    #compile model
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    #fit model
    model.fit(input[train], output[train], epochs=40, batch_size=32, verbose=0)
    #evaluate model
    scores = model.evaluate(input[test], output[test], verbose=0)
    print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
    list.append(scores[1]*100)
print("%.2f%% (+/- %.2f%%)" % (numpy.mean(list), numpy.std(list)))
#calculate prediction
predictions = model.predict(input)
#round predictions
rounded = [round(input[0]) for input in predictions]
#print(rounded)
