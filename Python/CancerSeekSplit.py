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

filename = os.path.join( os.getcwd(), '..', 'Data/CancerSEEK/Only Numbers (normal).csv' )
data = numpy.loadtxt(filename, delimiter=",")
#split data
input = data[:, 0:39]
output = data[:, 39]

#define 10-fold cross validation
kfold = StratifiedKFold(n_splits=10, shuffle=True, random_state = 7)

# Parameters: node number, regularizer, epochs
parameters = [30, 0.001, 50]
update = [5, 0.001, 10]

optimizeIndex = 1
temp = 0
while optimizeIndex <= 2:
    list = []
    for train, test in kfold.split(input, output):
        #build model
        model = Sequential()
        #model.add(Dropout(0.2, input_shape=(39,)))
        model.add(Dense(parameters[0], input_dim=39, activation='relu'))
        model.add(Dense(1, activation='sigmoid'))
        #compile model
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        #fit model
        model.fit(input[train], output[train], epochs=parameters[2], batch_size=32)
        #evaluate model
        scores = model.evaluate(input[test], output[test], verbose = 0)
        accuracy = scores[1]*100
        print("\n%s: %.2f%%" % (model.metrics_names[1], accuracy))
        list.append(accuracy)
    #print("weights: " + str(model.layers[0].get_weights()))
    accuracy = numpy.mean(list)
    print("average = " + str(accuracy))
    if temp == 0:
        temp = accuracy
        parameters[optimizeIndex] += update[optimizeIndex]
    elif accuracy-temp > 0.1:
        temp = accuracy
        parameters[optimizeIndex] += update[optimizeIndex]
    #    optimizeIndex += 1
    else:
        parameters[optimizeIndex] -= update[optimizeIndex]
    #    optimizeIndex -= 1
        temp = 0
    if optimizeIndex > 2:
        break
    print(str(optimizeIndex) + " " + str(parameters[optimizeIndex]))

print("\n" + "%.2f%% (+/- %.2f%%)" % (numpy.mean(list), numpy.std(list)))
#calculate prediction
predictions = model.predict(input)
#round predictions
rounded = [round(input[0]) for input in predictions]
#print(rounded)

#print parameters
for count in range(len(parameters)):
    print(str(count) + " " + str(parameters[count]))
