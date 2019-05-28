## James Quintero
## https://github.com/JamesQuintero
## Created: 5/2019
## Modified: 5/2019
##
## Handles all the data required for the program


from os import listdir
from os.path import isfile, join


from pcap_handler import PCAPHandler #for reading pcap files




class DataHandler:

	#object for PCAPHandler class
	pcap_handler = None

	#dictionary of file paths where keys are the filenames and values are the relative path
	dataset_paths = {}

	def __init__(self):
		self.pcap_handler = PCAPHandler()



	def get_packet_information(self, dataset):
		pass


	#
	def get_full_path(self, dataset_name):
		pass

	#returns list of datasets in alphabetical order
	def get_list_of_datasets(self):
		pass




if __name__=="__main__":

	pcap_handler = PCAPHandler()

	test_path = "./Datasets/2018-10-31-traffic-analysis-exercise.pcap"
	pcap_handler.read_pcap(test_path)

	