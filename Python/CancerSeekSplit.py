#!/usr/bin/env python3

from keras.models import Sequential
from keras.layers import Dense
from keras import regularizers
import numpy
import os
from DataSplit import getData

numpy.random.seed(7)

average = 0
num = 0
for i in range(5):
    #randomly split data into train, validation, test
    filename = os.path.join(os.getcwd(), '..', 'Data/CancerSEEK/Only Numbers (normal).csv')
    trainData, validationData, testData = getData(filename, 0.1, 0.2, False)

    '''filename = os.path.join(os.getcwd(), '..', 'Data/CancerSEEK/Training Data.csv' )
    trainData = numpy.loadtxt(filename, delimiter=",")
    filename = os.path.join(os.getcwd(), '..', 'Data/CancerSEEK/Validation Data.csv')
    validationData = numpy.loadtxt(filename, delimiter=",")
    filename = os.path.join(os.getcwd(), '..', 'Data/CancerSEEK/Test Data.csv')
    testData = numpy.loadtxt(filename, delimiter=",")'''


    #split data
    train = [trainData[:, 0:39], trainData[:, 39]]
    #validation = [validationData[:, 0:39], validationData[:, 39]]
    test = [testData[:, 0:39], testData[:, 39]]

    model = Sequential()
    model.add(Dense(35, input_dim=39, kernel_regularizer=regularizers.l2(0.0002), activation='relu'))
    model.add(Dense(20, kernel_regularizer=regularizers.l2(0), activation='relu'))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(train[0], train[1], epochs=150, batch_size=32, verbose = 0)

    accuracy = model.evaluate(train[0], train[1], verbose = 0)
    print("train: " + str(accuracy[1]*100))
    accuracy = model.evaluate(test[0], test[1], verbose = 0)
    print("test: " + str(accuracy[1]*100) + "\n")
    average += accuracy[1]*100
    num += 1
average /= num
print("average= " + str(average))
