## James Quintero
## https://github.com/JamesQuintero
## Created: 5/2019
## Modified: 5/2019
##
## Reads PCAP files containing network packets




import codecs

from kamene.all import * #library used to read pcap fils



class PCAPHandler:

	#maps int packet type identifier to its string version
	pkt_strings = {}

	def __init__(self):
		
		self.pkt_strings[1] = "ICMP"
		self.pkt_strings[2] = "ROUTER"
		self.pkt_strings[6] = "TCP"
		self.pkt_strings[17] = "UDP"


	def read_pcap(self, path):

		#reads the pcap file into list of packets
		packets = rdpcap(path)

		# print(packets)
		# packets.show()

		# packets.decode_payload_as()
		# packets.hexraw()





		## Packet contents ##
		###[ Ethernet ]###
		#   dst       = ff:ff:ff:ff:ff:ff
		#   src       = 00:50:8b:2a:96:0a
		#   type      = 0x800
		# ###[ IP ]###
		#      version   = 4
		#      ihl       = 5
		#      tos       = 0x0
		#      len       = 96
		#      id        = 7
		#      flags     =
		#      frag      = 0
		#      ttl       = 128
		#      proto     = udp
		#      chksum    = 0x1255
		#      src       = 10.100.9.107
		#      dst       = 10.100.9.255
		#      \options   \
		# ###[ UDP ]###
		#         sport     = netbios_ns
		#         dport     = netbios_ns
		#         len       = 76
		#         chksum    = 0xdd80
		# ###[ NBNS query request ]###
		#            NAME_TRN_ID= 64045
		#            FLAGS     = 10512
		#            QDCOUNT   = 1
		#            ANCOUNT   = 0
		#            NSCOUNT   = 0
		#            ARCOUNT   = 1
		#            QUESTION_NAME= b'HEADLESS-PC    '
		#            SUFFIX    = workstation
		#            NULL      = 0
		#            QUESTION_TYPE= NB
		#            QUESTION_CLASS= INTERNET
		# ###[ Raw ]###
		#               load      = b'\xc0\x0c\x00 \x00\x01\x00\x04\x93\xe0\x00\x06\x00\x00\nd\tk'



		all_packets = []

		for pkt in packets:
			# print(pkt.show())

			# print(pkt[IP].dst)
			# print()

			packet_info = {}
			# packet_info['']


			#packet_type = 17 for UDP, 6 for TCP, 1 for ICMP
			packet_info['packet_type'] = self.pkt_strings[pkt[IP].proto]
			#hexadecimal checksum is converted to decimal. 
			packet_info['checksum'] = pkt[IP].chksum
			packet_info['length'] = pkt[IP].len
			packet_info['source'] = pkt[IP].src
			packet_info['destination'] = pkt[IP].dst

			#list containing packet specific information based on the packet type
			packet_info['packet_info'] = {}

			#if packet is of type UDP
			if packet_info['packet_type']=="UDP":
				packet_info['packet_info']['source_port'] = pkt[UDP].sport
				packet_info['packet_info']['destination_port'] = pkt[UDP].dport
				packet_info['packet_info']['udp_len'] = pkt[UDP].len
				packet_info['packet_info']['udp_checksum'] = pkt[UDP].chksum

			#if packet is of type TCP
			elif packet_info['packet_type']=="TCP": 
				packet_info['packet_info']['source_port'] = pkt[TCP].sport
				packet_info['packet_info']['destination_port'] = pkt[TCP].dport
				packet_info['packet_info']['ack'] = pkt[TCP].ack
				packet_info['packet_info']['flags'] = pkt[TCP].flags
				packet_info['packet_info']['tcp_checksum'] = pkt[TCP].chksum
				packet_info['packet_info']['tcp_options'] = pkt[TCP].options

			#if packet is of type ICMP
			elif packet_info['packet_type']=="ICMP":
				packet_info['packet_info']['icmp_type'] = pkt[ICMP].type
				packet_info['packet_info']['icmp_checksum'] = pkt[ICMP].chksum

			#get the load if there is one
			try:
				packet_info['load'] = pkt[Raw].load
			except Exception as error:
				packet_info['load'] = None


			all_packets.append(packet_info)







		for x in range(0, len(all_packets)):
			print("Information: ")
			packet_info = all_packets[x]
			for key in packet_info:
				print(key+": "+str(packet_info[key]))
			print()


		return packet_info




		# for x in range(0, len(packets)):
		# 	# print(packets[x])
		# 	pkt = packets[x]

		# 	# #prints packets in hex format
		# 	# print(hexdump(pkt))

		# 	#prints the bytes version of the already byte default packet
		# 	# print(bytes(pkt))

		# 	print(Ether(pkt))



		# 	input()

		print("Num packets: "+str(len(packets)))


if __name__=="__main__":

	pcap_handler = PCAPHandler()

	test_path = "./Datasets/2018-10-31-traffic-analysis-exercise.pcap"
	pcap_handler.read_pcap(test_path)

	