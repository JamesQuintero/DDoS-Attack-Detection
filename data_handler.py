## James Quintero
## https://github.com/JamesQuintero
## Created: 5/2019
## Modified: 4/2021
##
## Handles all the data required for the program


import os
import os.path
import csv                      #script for CSV file handling

from os import listdir
from os.path import isfile, join

import time
import datetime


import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
import joblib

from pcap_handler import PCAPHandler #for reading pcap files




class DataHandler:

	#object for PCAPHandler class
	pcap_handler = None

	base_path = "./Datasets/"
	label_path = "./Labels/"
	live_sniffing_path = "./Live sniffing"


	IP_type = {}

	#list of dataset names that correspond to the filename
	datasets = []

	#list of pcap files in each dataset
	pcap_files = []

	#keys are dataset indices, and values are lists of initial label data
	initial_labels = {}

	def __init__(self):
		self.pcap_handler = PCAPHandler()

		self.load_list_of_datasets()
		self.load_list_of_pcaps()

		self.IP_type[0] = "Hop-by-Hop Option Header"
		self.IP_type[1] = "ICMP"
		self.IP_type[2] = "ROUTER"
		self.IP_type[6] = "TCP"
		self.IP_type[17] = "UDP"
		self.IP_type[58] = "ICMPv6"


	#param is a full path to a live pcap file
	#returns normalized input data 
	def get_live_input_data(self, pcap_path):
		if pcap_path=="":
			return


		data = self.pcap_handler.read_pcap(pcap_path)

		compressed_packets = self.compress_packets(data)
		input_data = self.generate_input_data(compressed_packets)

		normalized_input, normalized_output = self.normalize_compressed_packets(input_data, [])

		return normalized_input




	#returns 2D list where list element is the list of pcap information for a specific pcap file based on index
	#if pcap_index is None, then read and return contents of all pcap files in the dataset folder
	def get_packet_information(self, dataset_index, pcap_index=None):



		#if retrieving information from a specific pcap file
		if pcap_index!=None:
			pcap_path = self.get_pcap_path(dataset_index, pcap_index)

			print("Reading pcap "+str(pcap_path))

			data = self.pcap_handler.read_pcap(pcap_path)

			print("Finished reading pcap file")
			print()
			# input()

			return data

		#if retrieving all pcap information from a dataset
		else:

			pcap_paths = []
			for x in range(0, len(self.pcap_files[dataset_index])):
				pcap_paths.append(self.get_pcap_path(dataset_index, x))


			pcap_information = []

			#retrieves all packet information from the pcap files
			for x in range(0, len(pcap_paths)):
				pcap_path = pcap_paths[x]
				print("Reading pcap "+str(pcap_path))

				data = self.pcap_handler.read_pcap(pcap_path)

				print("Finished reading pcap file")
				print()
				# input()

				pcap_information.extend(data)


			# total_packets = 0
			# for x in range(0, len(pcap_information)):
			# 	total_packets += len(pcap_information[x])
			total_packets = len(pcap_information)
			print("Total number of packets: "+str(total_packets))

			return pcap_information



	#turns each packet data from dictionaries into a flat 1d list. 
	def compress_packets(self, packets):
		print("compress_packets()")

		new_packets = []
		for x in range(0, len(packets)):
			packet = packets[x]

			compressed_packet = self.pcap_handler.compress_packet(packet)
			new_packets.append(compressed_packet)

		return new_packets

	#turns 2d list of labels into 1d long list of labels
	def compress_labels(self, labels):
		return labels


	#returns actual neural network input data generated from compressed packet data
	#this neural network data includes frequency of IP addresses, packet types, etc. 
	def generate_input_data(self, compressed_packets):

		ethernet_source_addresses = {}
		ethernet_destination_addresses = {}

		IP_source_addresses = {}
		IP_destination_addresses = {}

		IP_type = {}





		#counts the number of occurrences of value in lookback_amount at lookback_index
		def count_occurrences(value, cur_index, lookback_amount, lookback_column):

			num = 0
			for x in range(cur_index, max(cur_index-lookback_amount, -1), -1):
				if compressed_packets[x][lookback_column]==value:
					num+=1
			return num




		to_return = []
		for x in range(0, len(compressed_packets)):
			row = []

			# self.print_compressed_packet(compressed_packets[x])

			ethernet_source = compressed_packets[x][1]
			ethernet_destination = compressed_packets[x][2]
			IP_source = compressed_packets[x][7]
			IP_destination = compressed_packets[x][8]

			# #if not logged this source address yet, then add it
			# if ethernet_source not in ethernet_source_addresses.keys():
			# 	ethernet_source_addresses[ethernet_source] = 1
			# else:
			# 	ethernet_source_addresses[ethernet_source] += 1

			# #if not logged this source address yet, then add it
			# if ethernet_destination not in ethernet_destination_addresses.keys():
			# 	ethernet_destination_addresses[ethernet_destination] = 1
			# else:
			# 	ethernet_destination_addresses[ethernet_destination] += 1

			# ethernet_difference = ethernet_source_addresses[ethernet_source] - ethernet_destination_addresses[ethernet_destination]


			# #if not logged this source address yet, then add it
			# if IP_source not in IP_source_addresses.keys():
			# 	IP_source_addresses[IP_source] = 1
			# else:
			# 	IP_source_addresses[IP_source] += 1

			# #if not logged this source address yet, then add it
			# if IP_destination not in IP_destination_addresses.keys():
			# 	IP_destination_addresses[IP_destination] = 1
			# else:
			# 	IP_destination_addresses[IP_destination] += 1

			# IP_difference = IP_source_addresses[IP_source] - IP_destination_addresses[IP_destination]

			# row.append(ethernet_source_addresses[ethernet_source])
			# row.append(ethernet_destination_addresses[ethernet_destination])
			# row.append(ethernet_difference)
			# row.append(IP_source_addresses[IP_source])
			# row.append(IP_destination_addresses[IP_destination])
			# row.append(IP_difference)




			lookback_amount = 100
			ethernet_source_occurrences = count_occurrences(value=ethernet_source, cur_index=x, lookback_amount=lookback_amount, lookback_column=1)
			ethernet_destination_occurrences = count_occurrences(value=ethernet_destination, cur_index=x, lookback_amount=lookback_amount, lookback_column=2)
			IP_source_occurrences = count_occurrences(value=IP_source, cur_index=x, lookback_amount=lookback_amount, lookback_column=7)
			IP_destination_occurrences = count_occurrences(value=IP_destination, cur_index=x, lookback_amount=lookback_amount, lookback_column=8)

			row.append(ethernet_source_occurrences)
			row.append(ethernet_destination_occurrences)
			row.append(IP_source_occurrences)
			row.append(IP_destination_occurrences)




			lookback_amount = 1000
			ethernet_source_occurrences = count_occurrences(value=ethernet_source, cur_index=x, lookback_amount=lookback_amount, lookback_column=1)
			ethernet_destination_occurrences = count_occurrences(value=ethernet_destination, cur_index=x, lookback_amount=lookback_amount, lookback_column=2)
			IP_source_occurrences = count_occurrences(value=IP_source, cur_index=x, lookback_amount=lookback_amount, lookback_column=7)
			IP_destination_occurrences = count_occurrences(value=IP_destination, cur_index=x, lookback_amount=lookback_amount, lookback_column=8)

			row.append(ethernet_source_occurrences)
			row.append(ethernet_destination_occurrences)
			row.append(IP_source_occurrences)
			row.append(IP_destination_occurrences)








			


			timestamp = compressed_packets[x][3]
			prev_timestamp1 = compressed_packets[max(0, x-1)][3]
			prev_timestamp10 = compressed_packets[max(0, x-10)][3]
			prev_timestamp100 = compressed_packets[max(0, x-100)][3]
			prev_timestamp1000 = compressed_packets[max(0, x-1000)][3]
			timestamp_difference1 = timestamp-prev_timestamp1
			timestamp_difference10 = timestamp-prev_timestamp10
			timestamp_difference100 = timestamp-prev_timestamp100
			timestamp_difference1000 = timestamp-prev_timestamp1000

			row.append(timestamp_difference1)
			row.append(timestamp_difference10)
			row.append(timestamp_difference100)
			row.append(timestamp_difference1000)

			to_return.append(row)



		return to_return






	#param is a 2D list of packet data, and returned value is a 2D list of the same data, but normalized. 
	def normalize_compressed_packets(self, compressed_packets, labels, dataset_index=0):
		unnormalized_input_data = compressed_packets.copy()
		unnormalized_output_data = labels.copy()
		input_data = compressed_packets
		output_data = labels

		#saves normalization params
		dataset_name = self.get_dataset_filename(dataset_index)
		input_scaler_filename = "./Models/input_normalization_params_{}.saver".format(dataset_name)

		#if have a saved normalization file, then use it
		if os.path.isfile(input_scaler_filename):
			print("Loaded scaler object file")
			input_scaler = joblib.load(input_scaler_filename)
			input_data = input_scaler.transform(input_data)
		#normalize the data
		else:
			input_scaler = StandardScaler()

			try:
				input_data = input_scaler.fit_transform(input_data)
				input_data = np.array(input_data).tolist()
			except Exception as error:
				print("Error when normalizing: {}".format(error))

			#saves normalization params for future use
			joblib.dump(input_scaler, input_scaler_filename)

		#convert string label to int target
		output_data = []
		for x in range(0, len(labels)):
			if labels[x][1]=="BENIGN":
				output_data.append(0)
			else:
				output_data.append(1)


		return input_data, output_data



	#loads labels corresponding to dataset and specific pcap file
	#if pcap_index is None, then return labels for all pcap files corresponding to the dataset index
	def get_labels(self, dataset_index, pcap_index=None):
		labels = []

		#if getting labels for a specific pcap file
		if pcap_index!=None:
			print("pcap_index!=None")
			label_path = self.get_label_path(dataset_index, pcap_index)
			print("Label path: "+str(label_path))

			labels = self.read_from_csv(label_path)
		#if retrieving labels for all pcap files belonging to dataset_index
		else:
			labels = []
			for x in range(0, len(self.pcap_files[dataset_index])):
				label_path = self.get_label_path(dataset_index, x)
				print("Label path: "+str(label_path))

				temp_labels = self.read_from_csv(label_path)

				labels.extend(temp_labels)

		return labels


	#iterates through all pcaps in the specified dataset, and calculates the corresponding labels.
	#results are saved to a csv. 
	def calculate_labels(self, dataset_index):

		#list of pcap names
		pcap_names = self.pcap_files[dataset_index]

		#name of the dataset corresponding to dataset_index
		dataset_name = self.datasets[dataset_index]



		for x in range(0, len(pcap_names)):

			labels = self.calculate_labels_helper(dataset_index, x)

			#saves labels to 
			new_label_path = self.label_path+"/"+str(dataset_name)+"/"+str(pcap_names[x])+".csv"
			self.save_to_csv(new_label_path, labels)



	#gets packet information, finds its corresponding information in a csv file, and gets its label to save in a central csv file. 
	#initial labels are appended to suplementary and central packet information in a csv file, but these packets are not in any order, 
	#	and don't contain all packets with labels. 
	#the final label csv file will be in chronological order
	def calculate_labels_helper(self, dataset_index, pcap_index):


		#if don't already have initial labels saved, then load them
		if dataset_index not in self.initial_labels.keys() or len(self.initial_labels[dataset_index])==0:
			self.initial_labels[dataset_index] = self.read_initial_labels(dataset_index)


		initial_labels = self.initial_labels[dataset_index]

		dataset_name = self.datasets[dataset_index]


		#creates labels folder if it doesn't already exist
		labels_folder = self.label_path+"/"+str(dataset_name)
		if os.path.exists(labels_folder)==False:
			os.mkdir(labels_folder)


		#gets packets
		dataset_contents = self.get_packet_information(dataset_index, pcap_index)




		#create dictionary where key is the source address, and value is another dictionary where key is destination address, and value is a list of packets with that source and destination address. 
		#this is for easy search
		label_dictionary = {}
		for x in range(0, len(initial_labels)):
			source = initial_labels[x]['source']
			destination = initial_labels[x]['destination']

			#if no key for source address yet, then initialize it
			if source not in label_dictionary.keys():
				label_dictionary[source] = {}

			if destination not in label_dictionary[source].keys():
				label_dictionary[source][destination] = []

			label_dictionary[source][destination].append(initial_labels[x])



		#returns the index of the label based on the packet contents
		def get_label(packet):
			label = "BENIGN"

			# print()
			# print("get_label()")
			# self.print_packet(packet)



			# overall_type = packet['Ethernet']['overall_type']
			# source = packet[overall_type]['source']


			packet_source = packet['IP']['source']
			packet_destination = packet['IP']['destination']
			# print("Source: "+str(packet_source))
			# print("Destination: "+str(packet_destination))

			labels_with_same_source = []
			try:
				labels_with_same_source = label_dictionary[packet_source][packet_destination]

				# print("Destinations corresponding to "+str(packet_source))
				# for key in label_dictionary[packet_source]:
				# 	print(key)
			except Exception as error:
				print("No label for source "+str(packet_source)+" and destination "+str(packet_destination))
				return label

			# print("Num labels with same source: "+str(len(labels_with_same_source)))


			
			packet_type = packet['IP']['packet_type'] 
			packet_timestamp = int(packet['Ethernet']['timestamp']) #format is unix timestamp
			try:
				packet_source_port = packet['packet_info']['source_port'] 
				packet_destination_port = packet['packet_info']['destination_port'] 
			except Exception as error:
				print("Error "+str(error))
				return label

			#adds 4 hours onto packet timestamp to be inline with the label timestamps
			packet_timestamp += 60*60*4

			# print("Searching through "+str(len(labels_with_same_source))+" packets")
			# print("Packet timestamp: "+str(packet_timestamp))

			
			for x in range(0, len(labels_with_same_source)):

				# print("Protocol: "+str(packet_type)+" | "+str(self.IP_type[labels_with_same_source[x]['protocol']]))
				# print("Source port: "+str(packet_source_port)+" | "+str(labels_with_same_source[x]['source_port']))
				# print("Destination port: "+str(packet_destination_port)+" | "+str(labels_with_same_source[x]['destination_port']))
				

				#if destination matches and protocol matches
				if packet_type==self.IP_type[labels_with_same_source[x]['protocol']] and\
					packet_source_port==labels_with_same_source[x]['source_port'] and\
					packet_destination_port==labels_with_same_source[x]['destination_port']:
					# print("Label: "+str(labels_with_same_source[x]))

					label_timestamp = time.mktime(datetime.datetime.strptime(labels_with_same_source[x]['timestamp'], "%d/%m/%Y %I:%M").timetuple())
					# print("Label Timestamp: "+str(label_timestamp))

					#checks if timestamps also match +- 10 minutes
					if abs(packet_timestamp-label_timestamp)<=600:
						label = labels_with_same_source[x]['label']
						# print("MATCHED")
						break


			# input()

			#defaults to BENIGN if label wasn't found
			return label








		#iterates through packets to find their corresponding labels
		new_labels = []
		for x in range(0, len(dataset_contents)):
			row = []
			row.append(x) #packet number

			if x%100 == 0:
				print("At packet {}/{}".format(x, len(dataset_contents)))

			# print("dataset contents[x]: "+str(dataset_contents[x]))

			#if the packet is an Ethernet packet
			if len(dataset_contents[x]['Ethernet'])>0:
				overall_type = dataset_contents[x]['Ethernet']['overall_type']
			#if packet is not an ethernet packet, consider it benign, and move on
			else:
				row.append("BENIGN")
				new_labels.append(row)
				continue


			label = "BENIGN"

			#only care about IP packets
			if overall_type=="IP":
				label = get_label(dataset_contents[x])


			row.append(label)
			new_labels.append(row)
			

		return new_labels



	def read_initial_labels(self, dataset_index):
		#returns empty path if invalid dataset index
		if dataset_index<0 or dataset_index >= len(self.datasets):
			print("Invalid dataset index in get_dataset_path()")
			return []

		dataset_name = self.datasets[dataset_index]
		label_path = self.label_path+"/"+str(dataset_name)+".csv"
		print("label path: "+str(label_path))


		contents = self.read_from_csv(label_path)

		#removes header row
		contents.pop(0)

		print("Num packets: "+str(len(contents)))

		new_contents = []

		#iterates through contents, and assigns each csv row to a dictionary for easy retrieval
		for x in range(0, len(contents)):

			row = {}
			row['source'] = contents[x][1]
			row['source_port'] = int(contents[x][2])
			row['destination'] = contents[x][3]
			row['destination_port'] = int(contents[x][4])
			row['protocol'] = int(contents[x][5])
			row['timestamp'] = contents[x][6]
			row['label'] = contents[x][-1]

			new_contents.append(row)


		return new_contents












	#returns matrix that was read from csv file at path
	def read_from_csv(self, path):
		if os.path.isfile(path):
			with open(path, newline='') as file:
				contents = csv.reader(file)

				temp_list=[]
				for row in contents:
					temp_matrix=[]
					for stuff in row:
						 temp_matrix.append(stuff)
					temp_list.append(temp_matrix)

				return temp_list
		else:
			return []

	#saves matrix to csv file
	def save_to_csv(self, path, data):
		with open(path, 'w', newline='') as file:
			contents = csv.writer(file)
			contents.writerows(data)



	def print_packet(self, packet):
		if "Ethernet" in packet.keys() and len(packet['Ethernet'])>0:
			print("  Type: "+str(packet['Ethernet']['overall_type']))
			print("  Source: "+str(packet['Ethernet']['source']))
			print("  Destination: "+str(packet['Ethernet']['destination']))
			print("  Timestamp: "+str(packet['Ethernet']['timestamp']))

			#print IP section if have it
			if len(packet['IP'])>0:
				IP_type = packet['IP']['packet_type']
				print()
				print("  IP: ")
				print("    Type: "+str(IP_type))
				print("    Source: "+str(packet['IP']['source']))
				print("    Destination: "+str(packet['IP']['destination']))
				print("    Length: "+str(packet['IP']['length']))
				print("    Checksum: "+str(packet['IP']['checksum']))


				#prints packet information
				print("    "+str(IP_type)+" Packet info: ")
				indent = "      "
				for key in packet['packet_info']:
					print(indent+str(key)+": "+str(packet['packet_info'][key]))



			#print IPv6 section if have it
			elif len(packet['IPv6'])>0:
				IPv6_type = packet['IPv6']['packet_type']
				print()
				print("  IPv6: ")
				print("    Type: "+str(IPv6_type))
				print("    Source: "+str(packet['IPv6']['source']))
				print("    Destination: "+str(packet['IPv6']['destination']))
				print("    Traffic Class: "+str(packet['IPv6']['traffic_class']))
				print("    Payloud Length: "+str(packet['IPv6']['payload_length']))
				print("    Next Header: "+str(packet['IPv6']['next_header']))
				print("    Hop Limit: "+str(packet['IPv6']['hop_limit']))

				#prints packet information
				print("    "+str(IPv6_type)+" Packet info: ")
				indent = "      "
				for key in packet['packet_info']:
					print(indent+str(key)+": "+str(packet['packet_info'][key]))



			#print ARP section if have it
			elif len(packet['ARP'])>0:
				print()
				print("  ARP: ")
				print("    Operation: "+str(packet['ARP']['operation']))
				print("    Hardware Source: "+str(packet['ARP']['hardware_source']))
				print("    HardwareDestination: "+str(packet['ARP']['hardware_destination']))
				print("    Protocol Source: "+str(packet['ARP']['protocol_source']))
				print("    Protocol Destination: "+str(packet['ARP']['protocol_destination']))
				print("    Length: "+str(packet['ARP']['length']))


		else:
			pass



		print("Load: "+str(packet['load']))
		print()


	#returns path of the most recent pcap file in "./Live sniffing"
	#the most recent pcap file will be the one last when sorted
	def get_latest_live_pcap(self):

		path = self.live_sniffing_path

		#gets list of pcap files in the dataset folder
		only_files = [f for f in listdir(path) if isfile(join(path, f))]

		pcap_list = []
		for file in only_files:
			if ".pcap" in file:
				pcap_list.append(file)

		#sorts pcap files alphanumerically
		pcap_list.sort()


		if len(pcap_list)>0:
			return path+"/"+pcap_list[-1]
		else:
			return ""



	#returns number of pcaps associated with the specified dataset_index
	def get_num_pcaps(self, dataset_index):
		#if invalid dataset_index
		if dataset_index<0 or dataset_index>=len(self.datasets):
			print("Invalid dataset_index: "+str(dataset_index))
			return 0

		return len(self.pcap_files[dataset_index])


	def print_compressed_packet(self, compressed_packet):
		for x in range(0, len(compressed_packet)):
			print(str(x)+": "+str(compressed_packet[x]))


	#returns the full path to the provided dataset index
	def get_dataset_path(self, dataset_index):

		dataset_name = self.get_dataset_filename(dataset_index)

		#if couldn't get the filename
		if dataset_name=="":
			return ""

		return self.base_path+"/"+str(dataset_name)

	#returns the filename of the specified dataset
	def get_dataset_filename(self, dataset_index):
		#returns empty path if invalid dataset index
		if dataset_index<0 or dataset_index >= len(self.datasets):
			print("Invalid dataset index")
			return ""

		dataset_name = self.datasets[dataset_index]

		return dataset_name

	#returns the full path to the provided pcap file
	def get_pcap_path(self, dataset_index, pcap_index):
		dataset_name = self.get_dataset_filename(dataset_index)
		pcap_name = self.get_pcap_filename(dataset_index, pcap_index)

		#if couldn't get dataset name
		if dataset_name=="":
			return ""

		#if couldn't get the filename
		if pcap_name=="":
			return ""

		return self.base_path+"/"+str(dataset_name)+"/"+str(pcap_name)+".pcap"
		

	#returns the filename of the specified pcap file from the specified dataset
	def get_pcap_filename(self, dataset_index, pcap_index):
		#returns empty path if invalid dataset index
		if dataset_index<0 or dataset_index >= len(self.pcap_files):
			print("Invalid dataset index")
			return ""

		#returns empty path if invalid pcap index
		if pcap_index<0 or pcap_index>= len(self.pcap_files[dataset_index]):
			print("Invalid pcap file index")
			return ""

		pcap_filename = self.pcap_files[dataset_index][pcap_index]
		return pcap_filename

	#returns the full path of the label csv file corresponding to dataset_index and pcap_index
	def get_label_path(self, dataset_index, pcap_index):
		dataset_name = self.get_dataset_filename(dataset_index)
		pcap_name = self.get_pcap_filename(dataset_index, pcap_index)

		#if couldn't get dataset name
		if dataset_name=="":
			return ""

		#if couldn't get the filename
		if pcap_name=="":
			return ""

		return self.label_path+"/"+str(dataset_name)+"/"+str(pcap_name)+".csv"



	#returns list of datasets in alphabetical order
	#each dataset is a folder of pcap files at self.base_path
	def load_list_of_datasets(self):
		path = self.base_path
		# onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

		only_folders = [f for f in listdir(path) if not isfile(join(path, f))]

		#sorts files in alphanumeric order
		only_folders.sort()

		#only supports pcap files
		self.datasets = []
		for folder in only_folders:
			# if ".pcap" in file:
			self.datasets.append(folder)



	#loads list of pcap filenames into global variable
	def load_list_of_pcaps(self):
		path = self.base_path

		self.pcap_files = []

		#iterates through list of dataset names
		for x in range(0, len(self.datasets)):

			dataset_path = path+"/"+self.datasets[x]


			#gets list of pcap files in the dataset folder
			only_files = [f for f in listdir(dataset_path) if isfile(join(dataset_path, f))]

			pcap_list = []
			for file in only_files:
				if ".pcap" in file:
					pcap_list.append(file.replace(".pcap", ""))

			#sorts pcap files alphanumerically
			pcap_list.sort()

			self.pcap_files.append(pcap_list)









if __name__=="__main__":

	pcap_handler = PCAPHandler()

	# test_path = "./Datasets/2018-10-31-traffic-analysis-exercise.pcap"
	# pcap_handler.read_pcap(test_path)

	data_handler = DataHandler()

	# data_handler.load_list_of_datasets()
	# data_handler.print_dataset_list()

	# print(data_handler.datasets)
	# print()
	# print(data_handler.pcap_files)

	data_handler.calculate_labels(1)

	