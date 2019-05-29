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

	base_path = "./Datasets/"

	# #dictionary of file paths where keys are the filenames and values are the relative path
	# dataset_paths = {}

	#list of dataset names that correspond to the filename
	datasets = []

	def __init__(self):
		self.pcap_handler = PCAPHandler()

		self.load_list_of_datasets()



	def get_packet_information(self, dataset_index):
		#gets the path of the specified dataset
		dataset_path = self.get_dataset_path(dataset_index)

		#retrieves all packet information from the pcap file
		pcap_information = self.pcap_handler.read_pcap(dataset_path)

		return pcap_information


	#returns the full path to the provided dataset index
	def get_dataset_path(self, dataset_index):

		#returns empty path if invalid dataset index
		if dataset_index<0 or dataset_index>= len(self.datasets):
			print("Invalid dataset index in get_dataset_path()")
			return ""

		dataset_name = self.datasets[dataset_index]

		return self.base_path+"/"+str(dataset_name)



	#returns list of datasets in alphabetical order
	def load_list_of_datasets(self):
		path = self.base_path
		onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

		#sorts files in alphanumeric order
		onlyfiles.sort()

		#only supports pcap files
		self.datasets = []
		for file in onlyfiles:
			if ".pcap" in file:
				self.datasets.append(file)


	#prints list of datasets
	def print_dataset_list(self):
		print("Datasets: ")
		for x in range(0, len(self.datasets)):
			print(str(x)+") "+str(self.datasets[x]))





if __name__=="__main__":

	pcap_handler = PCAPHandler()

	# test_path = "./Datasets/2018-10-31-traffic-analysis-exercise.pcap"
	# pcap_handler.read_pcap(test_path)

	data_handler = DataHandler()

	# data_handler.load_list_of_datasets()
	data_handler.print_dataset_list()

	