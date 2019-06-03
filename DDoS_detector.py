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



	def test(self, dataset_index, pcap_index=None):
		print("Dataset: "+str(self.data_handler.get_dataset_path(dataset_index)))
		print("PCAP: "+str(self.data_handler.get_pcap_path(dataset_index, pcap_index)))

		packets = self.data_handler.get_packet_information(dataset_index, pcap_index)


		#turns each packet data from dictionaries into a flat 1d list. 
		compressed_packets = self.data_handler.compress_packets(packets)



		normalized_input = self.data_handler.normalize_compressed_packets(packets)

		# for x in range(0, len(packets)):
		# 	self.data_handler.print_packet(packets[x])
		# 	input()


		labels = self.data_handler.get_labels(dataset_index, pcap_index)

		# print("Labels: ")
		# for x in range(0, len(labels)):
		# 	print(str(x)+": "+str(labels[x]))
		# 	input()
		# print()

		print("Num packets: "+str(len(packets)))
		print("Num labels: "+str(len(labels)))


if __name__=="__main__":

	DDoS_detector = DDoSDetector()


	DDoS_detector.test(1, 600)

	