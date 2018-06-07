#!/usr/bin/env python3

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LeakyReLU
from keras.layers import ELU
from keras import regularizers
import numpy
import os

numpy.random.seed(7)

filename = os.path.join( os.getcwd(), '..', 'Data/CancerSEEK/Only Numbers (normal).csv' )
data = numpy.loadtxt(filename, delimiter=",")

#split data
input = data[:, 0:39]
output = data[:, 39]

#build model
model = Sequential()
model.add(Dense(40, input_dim=39, kernel_regularizer=regularizers.l2(0.01), activation='relu'))
#model.add(ELU(alpha = 1.0))
model.add(Dense(25, kernel_regularizer=regularizers.l2(0.01), activation='relu'))
#model.add(ELU(alpha = 1.0))
model.add(Dense(1, activation='sigmoid'))
#compile model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
#fit model
model.fit(input, output, validation_split= 0.1, epochs=50, batch_size=10)
#evaluate model
scores = model.evaluate(input, output, validation_split=0.1)
#print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
#calculate prediction
predictions = model.predict(input)
#round predictions
rounded = [round(input[0]) for input in predictions]
#print(rounded)
