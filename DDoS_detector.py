## James Quintero
## https://github.com/JamesQuintero
## Created: 5/2019
## Modified: 5/2019
##
## Handles all the data required for the program

import sys
import os

from data_handler import DataHandler


class DDoSDetector:

	#DataHandler class object
	data_handler = None

	def __init__(self):
		self.data_handler = DataHandler()



	def test(self, dataset_index):
		print("Dataset: "+str(self.data_handler.get_dataset_path(dataset_index)))

		packet_information = self.data_handler.get_packet_information(dataset_index)


		# for x in range(0, len(all_packets)):
		# 	print("Information: ")
		# 	packet_info = all_packets[x]
		# 	for key in packet_info:
		# 		print(key+": "+str(packet_info[key]))
		# 	print()

		print("Num packets: "+str(len(packet_information)))


if __name__=="__main__":

	DDoS_detector = DDoSDetector()


	DDoS_detector.test(0)

	