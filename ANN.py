## James Quintero
## https://github.com/JamesQuintero
## Created: 5/2019
## Modified: 4/2021
##
## Handles all the neural network modeling

import sys
import os
import time

import numpy as np

# Importing the Keras libraries and packages
import keras
from keras.models import Sequential
from keras.models import load_model
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.layers import LeakyReLU
from keras.layers import PReLU
from keras.layers import Bidirectional

from data_handler import DataHandler



class ANN:

	data_handler = None

	def __init__(self):
		self.data_handler = DataHandler()


	#input is a 2D list of unnormalized data
	#output is binary/categorical list denoting DDoS type
	def train_model(self, input_data, output_data, dataset_index):

		train_size = 0.7 #percentage of dataset to use for training

		#splits data into train and test datasets for cross validation
		X_train = np.array(input_data[ : int(len(input_data)*train_size)])
		y_train = np.array(output_data[ : int(len(output_data)*train_size)])
		X_test = np.array(input_data[int(len(input_data)*train_size) : ])
		y_test = np.array(output_data[int(len(output_data)*train_size) : ])


		dataset_name = self.data_handler.get_dataset_filename(dataset_index)
		model_path = "./Models/{}.h5".format(dataset_name)


		#if model has never been trained, train it
		if os.path.exists(model_path)==False:

			print("Creating neural network")

			# Initialising the ANN
			model = Sequential()
			# Adding the input layer and the first hidden layer
			#the number of nodes in the input layer is the number of countries
			#hidden layer has num_countries/2 nodes
			model.add(Dense(input_dim = len(X_train[0]), units = int(len(X_train[0])/1), kernel_initializer = 'uniform', activation = 'relu'))
			model.add(Dropout(rate = 0.2))
			model.add(Dense(units = int(len(X_train[0])/1), kernel_initializer = 'uniform', activation = 'relu'))
			model.add(Dropout(rate = 0.2))
			# Adding the output layer
			#1 output layer node, since that'll be a percentage
			model.add(Dense(units = 1, kernel_initializer = 'uniform', activation = 'sigmoid'))
			# Compiling the ANN
			model.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
			# Fitting the ANN to the Training set
			print("Training neural network")
			model.fit(X_train, y_train, batch_size = 20, epochs = 20)

			#saves the model for future use
			model.save(model_path)

		#if model has already been trained, load it
		else:
			print("Model already exists, so load it\n")

			model = load_model(model_path)



		start_time = time.time()

		print("Testing neural network on hold-out portion of the dataset.")
		# Predicting the Test set results
		y_pred = model.predict(X_test)
		y_pred = (y_pred > 0.5)

		print("--- %s seconds to predict ---" % (time.time() - start_time))

		# Making the Confusion Matrix
		from sklearn.metrics import confusion_matrix
		cm = confusion_matrix(y_test, y_pred)


		print("Confusion matrix: ")
		print(str(cm))

		if len(cm) == 1:
			print("Undesirable confusion matrix, the neural network predicted on a single class for all data points. Try training with a better configuration, or testing with more occurances of both target classes.")
			return

		#True Negative
		TN = cm[0][0]
		#False Positive
		FP = cm[0][1]
		#False Negative
		FN = cm[1][0]
		#True Positive
		TP = cm[1][1]

		accuracy = (TN+TP)/(TN+FP+FN+TP)

		precision = TP/(FP+TP)

		sensitivity = TP/(TP+FN)

		#when it's a downmove, how often does model predict a downmove?
		specificity = TN/(TN+FP)

		#want to get 200%, 100% for sensitivity and 100% for specificity
		total = sensitivity + specificity

		print("Accuracy: "+str(accuracy))
		print("Precision: "+str(precision))
		print("Sensitivity: "+str(sensitivity))
		print("Specificity: "+str(specificity))
		print("Total: "+str(total))


	#model predicts labels, and results are saved to a csv
	def predict(self, dataset_index, input_data):

		#splits data into train and test datasets for cross validation
		input_data = np.array(input_data)

		dataset_name = self.data_handler.get_dataset_filename(dataset_index)
		model_path = "./Models/{}.h5".format(dataset_name)

		#if model has never been trained, train it
		if os.path.exists(model_path):
			model = load_model(model_path)
		else:
			print("Model {} doesn't exist".format(model_path))
			return []


		# Predicting the Test set results
		y_pred = model.predict(input_data)



		return y_pred







if __name__=="__main__":

	neural_network = ANN()


	neural_network.train_model([], [])