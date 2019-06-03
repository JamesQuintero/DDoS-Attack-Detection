## James Quintero
## https://github.com/JamesQuintero
## Created: 5/2019
## Modified: 6/2019
##
## Handles all the neural network modeling

import sys
import os

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

	#DataHandler class object
	data_handler = None

	def __init__(self):
		self.data_handler = DataHandler()


	#input is a 2D list of unnormalized data
	#output is binary/categorical list denoting DDoS type
	def train_model(self, input_data, output_data):

		print("Input: ")
		for x in range(0, 5):
			print(str(x)+": "+str(input_data[x]))
		print()

		# print("Output: ")
		# for x in range(0, len(output_data)):
		# 	print(str(x)+": "+str(output_data[x]))
		# print()



		train_size = 0.7 #percentage of dataset to use for training




		#splits data into train and test datasets for cross validation
		X_train = np.array(input_data[ : int(len(input_data)*train_size)])
		y_train = np.array(output_data[ : int(len(output_data)*train_size)])
		X_test = np.array(input_data[int(len(input_data)*train_size) : ])
		y_test = np.array(output_data[int(len(output_data)*train_size) : ])


		model_path = "./Models/model.h5"


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
			# model.add(Dense(units = int(len(X[0])/1), kernel_initializer = 'uniform', activation = 'relu'))
			# model.add(Dense(units = int(len(X[0])/1), kernel_initializer = 'uniform', activation = 'relu'))
			# Adding the output layer
			#1 output layer node, since that'll be a percentage
			model.add(Dense(units = 1, kernel_initializer = 'uniform', activation = 'sigmoid'))
			# Compiling the ANN
			model.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
			# Fitting the ANN to the Training set
			print("Training neural network")
			model.fit(X_train, y_train, batch_size = 5, epochs = 50)

			#saves the model for future use
			model.save(model_path)

		#if model has already been trained, load it
		else:
			print("Model already exists, so load it\n")

			model = load_model(model_path)




		# Predicting the Test set results
		y_pred = model.predict(X_test)
		y_pred = (y_pred > 0.5)

		# Making the Confusion Matrix
		from sklearn.metrics import confusion_matrix
		cm = confusion_matrix(y_test, y_pred)

		print("Confusion matrix: ")
		print(str(cm))




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





		# #predict whether US should be going into a recession today
		# US_recession_pred = model.predict(X)


		# to_save=[]
		# for x in range(0, len(US_recession_pred)):
		# 	row=[]
		# 	row.append(dates[x])
		# 	row.append(US_recession_pred[x][0])
		# 	to_save.append(row)

		# with open(data_save_path, 'w', newline='') as file:
		# 	contents = csv.writer(file)
		# 	contents.writerows(to_save)

		# print()
		# print()

		# print(str(US_recession_pred[-1][0]*100)+"% recession likelihood")

		# if US_recession_pred[-1][0]>0.5:
		# 	print("As of "+str(dates[-1])+", the United States is in a recession")
		# #because any percentage 1 or above is a considerable amount, be wary
		# elif US_recession_pred[-1][0]>0.01:
		# 	print("As of "+str(dates[-1])+", the United States is most likely heading into a recession")
		# else:
		# 	print("As of "+str(dates[-1])+", the United States is not in, or heading into, a recession")





if __name__=="__main__":

	neural_network = ANN()


	neural_network.train_model([], [])