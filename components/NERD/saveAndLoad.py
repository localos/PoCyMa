import numpy as np
import keras
import random
from keras import backend as K
from keras.models import Sequential
from keras.models import model_from_json
from keras.layers.core import Dense
from keras.layers import Activation
from editConfigParser import *

import os.path,sys

def save_w(path, model):

	model.save_weights(path)

def load_w(path, model):
	model.load_weights(path)
	return model
	
def save_m(path, model):

	model_json = model.to_json()
	with open(path, "w") as json_file:
		json_file.write(model_json)

def load_m(path):
	json_file = open(path, 'r')
	loaded_model_json = json_file.read()
	return loaded_model_json
	
def load_complete_model():
	
	inputs = getInt(("NET","numberofinputs"))+1 #+1 wegen SynRate to Do : wenn SynRate ausgelagert wird hier entfernen
	outputs = getInt(("NET","numberofoutputs"))
	model = Sequential([
		Dense(16,input_shape=(inputs,), activation='relu'),
		Dense(32, activation='relu'),
		Dense(outputs, activation='softmax')
		])	
		
	if os.path.exists("resource/weights"):
		model = load_w("resource/weights", model)
	
	return model
	
def save_p(input,prediction,prediction_c):
# alte Predictions und neues Predictions zusammenführen

	if os.path.exists("resource/pred.npz"):
		
		input_p = []
		prediction_p = []
		prediction_c_p = []
	
		with np.load("resource/pred.npz") as file:
			input_p = file["input"]
			prediction_p = file["prediction"]
			prediction_c_p = file["prediction_c"]
	
		for index, item in enumerate(input):
			input_p = np.append(input_p,[item],axis=0)
			prediction_p = np.append(prediction_p,[prediction[index]],axis=0)
			prediction_c_p = np.append(prediction_c_p,[prediction_c[index]],axis=0)
					
		os.remove("resource/pred.npz")
		input = input_p
		prediction = prediction_p
		prediction_c = prediction_c_p
		print(input.size)
		print(prediction.size)
		np.savez("resource/pred",input=input,prediction=prediction,prediction_c=prediction_c)
	
	else:
		np.savez("resource/pred",input=input,prediction=prediction,prediction_c=prediction_c)

def load_p():
	
	input = None
	prediction = None
	
	if os.path.exists("resource/pred.npz"):
		with np.load("resource/pred.npz") as file:
			input = file["input"]
			prediction = file["prediction"]
			prediction_c = file["prediction_c"]
		return input,prediction,prediction_c
	else:
		print("No file found")
		
def save_rp(net_input,net_pred,used_meth,user_rating):
# altes Trainingsset und neues Trainingsset zusammenführen
# Trainingsset hat Bewertung mit drin

	if not os.path.exists("resource/trainset.npz"):
		gen_test_set(False)

		
	train_samples = []
	train_labels = []
	method = []
	rating = []
	
	with np.load("resource/trainset.npz") as file:
		train_samples = file["train_samples"]
		train_labels = file["train_labels"]
		method = file["method"]
		rating = file["rating"]
	
		for index, item in enumerate(net_input):
			train_samples = np.append(train_samples,[item],axis=0)
			train_labels = np.append(train_labels,[net_pred[index]],axis=0)
			method = np.append(method,[used_meth[index]],axis=0)
			rating = np.append(rating,[user_rating[index]],axis=0)
		
	os.remove("resource/trainset.npz")
	print(train_labels.size)
	print(train_samples.size)
	print(method.size)
	print(rating.size)
	np.savez("resource/trainset",train_samples=train_samples,train_labels=train_labels,method=method,rating=rating)	
	os.remove("resource/pred.npz")
	
def load_rp():
		
	if os.path.exists("resource/ratedPred.npz"):
		return np.load("resource/ratedPred.npz")
		
	else:
		print("No file found")
		
def load_whole_ts(path):
	
	train_samples = []
	train_labels = []
	
	if os.path.exists(path):
		with np.load(path) as file:
			train_samples = file["train_samples"]
			train_labels = file["train_labels"]
		return np.array(train_samples),np.array(train_labels)
	
	else:
		print("no file found")

def load_ts(path):

	#reduzieren der Trainingssätze auf 1000 Einträge
	#inklusive Label Swapping bei allen Bewertungen > 0 in denen UserMethod und Label unterschiedlich sind
	train_samples = []
	train_labels = []
	method = []
	rating = []
	final_ts = []
	final_tl = []
	size = 0
	maxSize = 10000
	
	#Prüfen auf Verfügbarkeit des Trainingssets
	if os.path.exists(path):
		#Öffnen der Datei
		with np.load(path) as file:
			#Laden der Werte
			train_samples = file["train_samples"]
			train_labels = file["train_labels"]
			method = file["method"]
			rating = file["rating"]
		#Abarbeiten der Ratings von 5 -> 1
		for i in range(5,0,-1):
			for index in range(0,train_labels.size):
				#Prüfen auf maximale Größe
				if (str(rating[index]) == str(i)) and (size < maxSize):
					#Anhängen des Wertes 
					final_ts.append(train_samples[index])
					#Prüfen der Methode
					if(str(train_labels[index]) != method[index]):
						final_tl.append(ord(method[index])-48)
					else:
						final_tl.append(train_labels[index])
					size = size + 1
		#Random Auffüllen von Werten
		while size < maxSize:
			index_rand = random.randint(0,train_labels.size-1)
			if str(rating[index_rand]) == str(0):
				final_ts.append(train_samples[index])
				final_tl.append(train_labels[index])
				size = size + 1
		#Rückgabe des Sets
		return np.array(final_ts),np.array(final_tl)
		
	else:
		print("No file found")
	
def load_pf(path):
	if os.path.exists(path):
		return np.load(path)
		
	else:
		print("No file found")	
		sys.exit(2)