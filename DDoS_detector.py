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
		if pcap_index!=None:
			print("PCAP: "+str(self.data_handler.get_pcap_path(dataset_index, pcap_index)))

		packets = []
		labels = []

		# #if getting all pcap files for specified dataset_index
		# if pcap_index==None:
		# 	num_pcaps = self.data_handler.get_num_pcaps(dataset_index)

		# 	packets = []
		# 	for x in range(0, num_pcaps):
		# 		pcap_contents = self.data_handler.get_packet_information(dataset_index, x)
		# 		packets.append(pcap_contents)

		# 	labels = []
		# 	for x in range(0, num_pcaps):
		# 		pcap_labels = self.data_handler.get_labels(dataset_index, x)
		# 		labels.append(pcap_labels)


		# 	#turns each packet data from dictionaries into a flat 1d list. 
		# 	compressed_packets = self.data_handler.compress_packets(packets)

		# 	#turns 2d list of labels into 1d list
		# 	compressed_labels = self.data_handler.compress_labels(labels)


		# #if getting a specific pcap file
		# else:
		# 	packets = self.data_handler.get_packet_information(dataset_index, pcap_index)
		# 	labels = self.data_handler.get_labels(dataset_index, pcap_index)

		# 	#turns each packet data from dictionaries into a flat 1d list. 
		# 	compressed_packets = self.data_handler.compress_packets([packets])

		# 	#turns 2d list of labels into 1d list
		# 	compressed_labels = self.data_handler.compress_labels([labels])

		# 	# print("Num pcaps: "+str(len(packets)))
		# 	# print("Num packets: "+str(len(packets[0])))


		


		packets = self.data_handler.get_packet_information(dataset_index, pcap_index)
		labels = self.data_handler.get_labels(dataset_index, pcap_index)

		#turns each packet data from dictionaries into a flat 1d list. 
		compressed_packets = self.data_handler.compress_packets(packets)


		# print("First 5 compressed packets: ")
		# for x in range(0, 5):
		# 	print(str(x))
		# 	for y in range(0, len(compressed_packets[x])):
		# 		print(str(y)+": "+str(compressed_packets[x][y]))
		# 	print()
		# print()


		input_data = self.data_handler.generate_input_data(compressed_packets)

		# print("Input data ("+str(len(input_data))+" items): ")
		# for x in range(0, len(input_data)):
		# 	print(str(x)+": "+str(input_data[x]))
		# 	input()
		# print()



		normalized_input, normalized_output = self.data_handler.normalize_compressed_packets(input_data, labels)


		# print("First 5 compressed normalized packets: ")
		# for x in range(0, 5):
		# 	print(str(x))
		# 	for y in range(0, len(normalized_input[x])):
		# 		print(str(y)+": "+str(normalized_input[x][y]))
		# 	print()
		# print()


		# print("Labels: ")
		# for x in range(0, len(labels)):
		# 	print(str(x)+": "+str(labels[x]))
		# 	input()
		# print()

		print("Num packets: "+str(len(normalized_input)))
		print("Num labels: "+str(len(normalized_output)))





		#feeds input data and output data into the neural network
		self.neural_network.train_model(normalized_input, normalized_output)



	#dataset_index can specify a dataset to predict on, or if None, 
	# will represent predicting on live packets from "./Live sniffing"
	def predict(self, dataset_index=None, pcap_index=None):

		#if predicting from a dataset
		if dataset_index!=None:

			packets = self.data_handler.get_packet_information(dataset_index, pcap_index)
			labels = self.data_handler.get_labels(dataset_index, pcap_index)

			#turns each packet data from dictionaries into a flat 1d list. 
			compressed_packets = self.data_handler.compress_packets(packets)


			input_data = self.data_handler.generate_input_data(compressed_packets)

			normalized_input, normalized_output = self.data_handler.normalize_compressed_packets(input_data, labels)

			print("Num packets: "+str(len(normalized_input)))
			print("Num labels: "+str(len(normalized_output)))


			#feeds input data and output data into the neural network
			predicted_labels = self.neural_network.predict(normalized_input)

			# self.data_handler.save_prediction(dataset_index, pcap_index)


		#predicting live pcap files
		else:
			latest_pcap_path = self.data_handler.get_latest_live_pcap()

			if latest_pcap_path=="":
				print("There is no pcap file to predict from")
				return

			print("Latest pcap path: "+str(latest_pcap_path))

			#returns normalized input data from the specified pcap path
			normalized_input = self.data_handler.get_live_input_data(latest_pcap_path)


			print("Num packets: "+str(len(normalized_input)))

			latest_packet = [normalized_input[-1]]


			#feeds input data and output data into the neural network
			predicted_label = self.neural_network.predict(latest_packet)
			predicted_label = predicted_label[-1][0]

			print("Predicted label: "+str(predicted_label))








if __name__=="__main__":

	DDoS_detector = DDoSDetector()


	DDoS_detector.train(dataset_index=1, pcap_index=None)

	# DDoS_detector.predict()

	