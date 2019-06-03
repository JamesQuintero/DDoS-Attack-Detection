## James Quintero
## https://github.com/JamesQuintero
## Created: 5/2019
## Modified: 6/2019
##
## Handles all the neural network modeling

import sys
import os

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
		for x in range(0, len(input_data)):
			print(str(x)+": "+str(input_data[x]))
		print()

		# print("Output: ")
		# for x in range(0, len(output_data)):
		# 	print(str(x)+": "+str(output_data[x]))
		# print()






if __name__=="__main__":

	neural_network = ANN()


	neural_network.train_model([], [])