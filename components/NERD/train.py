import numpy as np
import random
from sklearn.preprocessing import MinMaxScaler
import keras
from keras import backend as K
from keras.models import Sequential
from keras.layers import Activation
from keras.layers.core import Dense
from keras.optimizers import Adam
from keras.metrics import categorical_crossentropy


def train(model,train_samples, train_labels, vlevel):

	for i in range(0,10):
	
		#Tupel erstellen und shufflen

		zip_list = list(zip(train_labels,train_samples))
		zip_list = random.sample(zip_list, len(zip_list))

		#Geshufflete Tupel wieder in Listen aufsplitten
		train_labels,train_samples = zip(*zip_list)
		
		#Numpy Arrays erstellen
		train_labels = np.array(train_labels)
		train_samples = np.array(train_samples)
		
		#Benutzte Algorithmen für Model einstellen
		model.compile(Adam(lr=.0001), loss='sparse_categorical_crossentropy', metrics=['accuracy'])
		
		#Model mit Werten trainieren
		model.fit(train_samples, train_labels, validation_split=0.1, batch_size=200, epochs=5, shuffle=True, verbose=vlevel)
	return model