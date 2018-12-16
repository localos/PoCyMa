import numpy as np
import os.path
import random
from dataTemplate import load_json_file

def gen_orig_set():
		
	datapaths = []
	datapaths.append("resource/tor.json")
	datapaths.append("resource/xerxes.json")
	datapaths.append("resource/webservice.json")
	datapaths.append("resource/normal_1_combined_verringert.json")
	datapaths.append("resource/nginx_combined.json")
	datapaths.append("resource/pr0nxpossi_combined.json")
	train_samples = []
	train_labels = []
	method  = []
	rating  = []
	
	for i in range(0,len(datapaths)):
		data = load_json_file(datapaths[i])
		for item in data:
			if(item[-1] == 2):
				train_samples.append(item[0:-1])
				train_labels.append(2)
				method.append(0)
				rating.append(0)				
			elif(item[-1] == 1):	
				train_samples.append(item[0:-1])
				train_labels.append(1)
				method.append(0)
				rating.append(0)
			else:
				train_samples.append(item[0:-1])
				train_labels.append(0)
				method.append(0)
				rating.append(0)	
				
	#Shufflen der erstellten Werte
	zip_list = list(zip(train_labels,train_samples))
	zip_list = random.sample(zip_list, len(zip_list))

	#Geshufflete Tupel wieder in Listen aufsplitten
	train_labels,train_samples = zip(*zip_list)
	
	train_samples = np.array(train_samples)
	train_labels = np.array(train_labels)
	np.savez("resource/trainsetOrig",train_samples=train_samples,train_labels=train_labels,method=method,rating=rating)

def gen_train_set_from_orig():
		
	train_samples = []
	train_labels = []
	method = []
	rating = []
		
	with np.load("resource/trainsetOrig.npz") as file:
		train_samples = file["train_samples"]
		train_labels = file["train_labels"]
		method = file["method"]
		rating = file["rating"]
	
	np.savez("resource/trainset.npz",train_samples=train_samples,train_labels=train_labels,method=method,rating=rating)