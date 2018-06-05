#!/usr/bin/env python3

from keras.models import Sequential
from keras.layers import Dense
import numpy
import os

filename = os.path.join( os.getcwd(), '..', 'Data/CancerSEEK/protein.arff' )
