## James Quintero
## https://github.com/JamesQuintero
## Created: 5/2019
## Modified: 6/2019
##
## Handles all the data required for the program

import sys
import os

from data_handler import DataHandler
from ANN import ANN


class DDoSDetector:

	#DataHandler class object
	data_handler = None

	#ANN class object
	neural_network = None

	def __init__(self):
		self.data_handler = DataHandler()
		self.neural_network = ANN()



	def train(self, dataset_index, pcap_index=None):
		print("Dataset: "+str(self.data_handler.get_dataset_path(dataset_index)))
		print("PCAP: "+str(self.data_handler.get_pcap_path(dataset_index, pcap_index)))

		packets = self.data_handler.get_packet_information(dataset_index, pcap_index)
		labels = self.data_handler.get_labels(dataset_index, pcap_index)


		#turns each packet data from dictionaries into a flat 1d list. 
		compressed_packets = self.data_handler.compress_packets(packets)


		print("First 5 compressed packets: ")
		for x in range(0, 5):
			print(str(x))
			for y in range(0, len(compressed_packets[x])):
				print(str(y)+": "+str(compressed_packets[x][y]))
			print()
		print()


		input_data = self.data_handler.generate_input_data(compressed_packets)

		# print("Input data ("+str(len(input_data))+" items): ")
		# for x in range(0, len(input_data)):
		# 	print(str(x)+": "+str(input_data[x]))
		# 	input()
		# print()



		input_scalar, output_scalar, normalized_input, normalized_output = self.data_handler.normalize_compressed_packets(input_data, labels)

		# for x in range(0, len(packets)):
		# 	self.data_handler.print_packet(packets[x])
		# 	input()

		print("First 5 compressed normalized packets: ")
		for x in range(0, 5):
			print(str(x))
			for y in range(0, len(normalized_input[x])):
				print(str(y)+": "+str(normalized_input[x][y]))
			print()
		print()


		print("First 5 normalized output: ")
		for x in range(0, 5):
			# print(str(x))
			# for y in range(0, len(normalized_output[x])):
			print(str(x)+": "+str(normalized_output[x]))
			# print()
		print()

		# print("Labels: ")
		# for x in range(0, len(labels)):
		# 	print(str(x)+": "+str(labels[x]))
		# 	input()
		# print()

		print("Num packets: "+str(len(normalized_input)))
		print("Num labels: "+str(len(normalized_output)))





		#feeds input data and output data into the neural network
		self.neural_network.train_model(normalized_input, normalized_output)






if __name__=="__main__":

	DDoS_detector = DDoSDetector()


	DDoS_detector.train(1, 0)

	