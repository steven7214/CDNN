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

# Parameters: node number, regulizer
parameters = [45, 40, 0]
update = [5, 5, 0.00005]

accuracy = 0
optimizeIndex = 0
while optimizeIndex <= 2:
    print(str(optimizeIndex) + " " + str(parameters[optimizeIndex]))
    #build model
    model = Sequential()
    #model.add(Dropout(0.2, input_shape=(39,)))
    model.add(Dense(parameters[0], input_dim=39, kernel_regularizer=regularizers.l2(parameters[2]), activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    #compile model
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    #fit model
    model.fit(train[0], train[1], epochs=parameters[1], batch_size=32, verbose = 0)
    #evaluate model
    scores = model.evaluate(validation[0], validation[1], verbose = 0)
    temp = scores[1]*100
    print("%s: %.2f%%\n" % (model.metrics_names[1], temp))
    #print("weights: " + str(model.layers[0].get_weights()))
    if accuracy == 0:
        accuracy = temp
        parameters[optimizeIndex] += update[optimizeIndex]
    elif temp-accuracy > -0.1:
        accuracy = temp
        parameters[optimizeIndex] += update[optimizeIndex]
    else:
        parameters[optimizeIndex] -= update[optimizeIndex]
        optimizeIndex += 1
        accuracy = 0
        #print parameters
        for count in range(len(parameters)):
            print(str(count) + " " + str(parameters[count]) + "\n")

accuracy = model.evaluate(train[0], train[1], verbose = 0)
print("train: " + str(accuracy[1]*100))
accuracy = model.evaluate(validation[0], validation[1], verbose = 0)
print("validation: " + str(accuracy[1]*100))
accuracy = model.evaluate(test[0], test[1], verbose = 0)
print("test: " + str(accuracy[1]*100))

#calculate prediction
predictions = model.predict(test[0])
#round predictions
rounded = [round(test[0]) for test in predictions]
#print(rounded)
