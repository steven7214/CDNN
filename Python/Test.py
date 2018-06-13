#!/usr/bin/env python3

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LeakyReLU
from keras.layers import ELU
from keras import regularizers
from keras.layers import Dropout
from sklearn.model_selection import StratifiedKFold
import numpy
import os

numpy.random.seed(7)

filename = os.path.join( os.getcwd(), '..', 'Data/CancerSEEK/Training Data.csv' )
trainData = numpy.loadtxt(filename, delimiter=",")
filename = os.path.join(os.getcwd(), '..', 'Data/CancerSEEK/Validation Data.csv')
validationData = numpy.loadtxt(filename, delimiter=",")
filename = os.path.join(os.getcwd(), '..', 'Data/CancerSEEK/Test Data.csv')
testData = numpy.loadtxt(filename, delimiter=",")

#split data
train = [trainData[:, 0:39], trainData[:, 39]]
validation = [validationData[:, 0:39], validationData[:, 39]]
test = [testData[:, 0:39], testData[:, 39]]

accuracy = 0
optimizeIndex = 0
while optimizeIndex <= 2:
    #build model
    model = Sequential()
    model.add(Dense(50, input_dim=39, kernel_regularizer=regularizers.l2(0), activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    #compile model
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    #fit model
    model.fit(train[0], train[1], epochs=40, batch_size=32, verbose = 0)
    #evaluate model
    scores = model.evaluate(validation[0], validation[1], verbose = 0)
    temp = scores[1]*100
    print("%s: %.2f%%\n" % (model.metrics_names[1], temp))
    optimizeIndex += 1
