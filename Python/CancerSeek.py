#!/usr/bin/env python3

from keras.models import Sequential
from keras.layers import Dense
import numpy
import os

filename = os.path.join( os.getcwd(), '..', 'Data/CancerSEEK/protein.csv' )
data = numpy.loadtxt(filename, delimiter=",")
print(data)
#split data
input = data[:, 0:39] #unfinished...must split into training and testing
output = data[:, 39]
#build model
model = Sequential()
#model.add(Dense(44, input_dim=40, activation = 'relu'))
#model.add(Dense(40, activation='relu'))
model.add(Dense(1, input_dim=40, activation='sigmoid'))
#compile model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
#fit model
model.fit(input, output, epochs=150, batch_size=10)
#evaluate model
scores = model.evaluate(input, output)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
