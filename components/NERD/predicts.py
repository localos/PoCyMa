import numpy as np
import random
from sklearn.preprocessing import MinMaxScaler
import keras
from keras import backend as K
	
def predict_data(model, predict_set):
		
	predictions = model.predict(predict_set,batch_size=1,verbose=0)
	predictions_c = model.predict_classes(predict_set,batch_size=1,verbose=0)

	return predict_set,predictions,predictions_c	