## James Quintero
## https://github.com/JamesQuintero
## Created: 5/2019
## Modified: 6/2019
##
## Reads PCAP files containing network packets




import codecs

from kamene.all import * #library used to read pcap fils



class PCAPHandler:

	#maps packet type to its string version
	pkt_type = {}

	#maps int IP packet type identifier to its string version
	IP_type = {}

	#dictionary where key are packet sections, and values are lists of strings that are keys for those packet sections
	supported_keys = {}

	def __init__(self):
		

		#initializes packet types
		#https://en.wikipedia.org/wiki/EtherType
		self.pkt_type[0] = "None"
		self.pkt_type[2048] = "IP"
		self.pkt_type[2054] = "ARP"
		self.pkt_type[34525] = "IPv6"
		self.pkt_type[35020] = "LLDP"

		#https://en.wikipedia.org/wiki/List_of_IP_protocol_numbers
		self.IP_type[0] = "Hop-by-Hop Option Header"
		self.IP_type[1] = "ICMP"
		self.IP_type[2] = "ROUTER"
		self.IP_type[6] = "TCP"
		self.IP_type[17] = "UDP"
		self.IP_type[58] = "ICMPv6"





		## If you change this section, then the order of input values for the neural network will also change ##
		#overall packet information
		ethernet_keys = ["overall_type", "source", "destination", "timestamp"]
		#Ethernet information
		IP_keys = ["packet_type", "length", "checksum", "source", "destination"]
		IPv6_keys = ["packet_type", "traffic_class", "payload_length", "next_header", "hop_limit", "source", "destination"]
		ARP_keys = ["length", "operation", "hardware_source", "protocol_source", "hardware_destination", "protocol_destination"]
		LLDP_keys = []
		#IP information
		UDP_keys = ["udp_len", "udp_checksum", "source_port", "destination_port"]
		# TCP_keys = ["tcp_checksum", "source_port", "destination_port", "ack", "flags", "tcp_options"]
		TCP_keys = ["tcp_checksum", "source_port", "destination_port", "ack", "flags"]
		ICMP_keys = ["icmp_type", "icmp_checksum"]
		#IPv6 information
		hop_by_hop_keys = []
		ICMPv6_keys = ["icmp_type", "icmp_checksum", "target"]
		#UDP information
		NTP_keys = ["leap", "mode", "stratum", "dispersion", "id"]


		self.supported_keys = {}
		#overall packet type
		self.supported_keys['ethernet_keys'] = ethernet_keys
		#Ethernet type
		self.supported_keys['IP_keys'] = IP_keys
		self.supported_keys['IPv6_keys'] = IPv6_keys
		self.supported_keys['ARP_keys'] = ARP_keys
		self.supported_keys['LLDP_keys'] = LLDP_keys
		#IP section
		self.supported_keys['UDP_keys'] = UDP_keys
		self.supported_keys['TCP_keys'] = TCP_keys
		self.supported_keys['ICMP_keys'] = ICMP_keys
		#IPv6 section
		self.supported_keys['hop_by_hop_keys'] = hop_by_hop_keys
		self.supported_keys['ICMPv6_keys'] = ICMPv6_keys
		#UDP section
		self.supported_keys['NTP_keys'] = NTP_keys



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

		# for pkt in packets:
		# for x in range(0, 10):
		for x in range(0, len(packets)):
			pkt = packets[x]


			# print(pkt[IP].dst)
			# print()

			packet_info = {}
			# packet_info['']

			packet_info['Ethernet'] = {}
			# packet_info['']
			packet_info['IP'] = {}
			packet_info['ARP'] = {}
			packet_info['IPv6'] = {}
			#list containing packet specific information based on the packet type
			packet_info['packet_info'] = {}


			overall_packet_type = ""

			
			#checks if packet is an ethernet packet
			try:
				pkt['Ethernet']
				overall_packet_type = "Ethernet"
			except Exception as error:
				#packet is not of type ethernet
				pass


			#checks if packet is a LAN packet
			try:
				pkt["802.3"]
				overall_packet_type = "802.3"
			except Exception as error:
				#packet is not of type ethernet
				pass





			if overall_packet_type=="Ethernet":
				self.read_Ethernet_packet(packet_info, pkt)

				
			if overall_packet_type=="802.3":
				self.read_LAN_packet(packet_info, pkt)







			if overall_packet_type=="Ethernet":

				#if packet is of type IP
				if packet_info['Ethernet']['overall_type']=="IP":
					self.read_IP_packet(packet_info, pkt)

				#if packet is of type ARP (Address Resolution Protocol)
				#Address Resolution Protocol packet contents: https://en.wikipedia.org/wiki/Address_Resolution_Protocol
				elif packet_info['Ethernet']['overall_type']=="ARP":
					self.read_ARP_packet(packet_info, pkt)

				elif packet_info['Ethernet']['overall_type']=="IPv6":
					self.read_IPv6_packet(packet_info, pkt)

				elif packet_info['Ethernet']['overall_type']=="LLDP":
					self.read_LLDP_packet(packet_info, pkt)



			elif overall_packet_type=="802.3":
				pass

			else:
				pass


			

			




			#get the load if there is one
			try:
				packet_info['load'] = pkt[Raw].load
			except Exception as error:
				packet_info['load'] = None


			all_packets.append(packet_info)



		return all_packets




		# for x in range(0, len(packets)):
		# 	# print(packets[x])
		# 	pkt = packets[x]

		# 	# #prints packets in hex format
		# 	# print(hexdump(pkt))

		# 	#prints the bytes version of the already byte default packet
		# 	# print(bytes(pkt))

		# 	print(Ether(pkt))



		# print("Num packets: "+str(len(packets)))



	#compresses a dictionary packet into a list packet
	def compress_packet(self, packet):


		# supported_keys = []
		# #overall packet type
		# supported_keys.extend(ethernet_keys)
		# #Ethernet type
		# supported_keys.extend(IP_keys)
		# supported_keys.extend(IPv6_keys)
		# supported_keys.extend(ARP_keys)
		# supported_keys.extend(LLDP_keys)
		# #IP section
		# supported_keys.extend(UDP_keys)
		# supported_keys.extend(TCP_keys)
		# supported_keys.extend(ICMP_keys)
		# #IPv6 section
		# supported_keys.extend(hop_by_hop_keys)
		# supported_keys.extend(ICMPv6_keys)
		# #UDP section
		# supported_keys.extend(NTP_keys)


		


		packet_list = []
		#gets Ethernet keys if they exist
		try:
			to_extend = []
			for x in range(0, len(self.supported_keys['ethernet_keys'])):
				to_extend.append(packet['Ethernet'][self.supported_keys['ethernet_keys'][x]])
		except:
			to_extend = [0]*len(self.supported_keys['ethernet_keys'])
		packet_list.extend(to_extend)


		#gets IP keys if they exist
		try:
			to_extend = []
			for x in range(0, len(self.supported_keys['IP_keys'])):
				to_extend.append(packet['IP'][self.supported_keys['IP_keys'][x]])
		except:
			to_extend = [0]*len(self.supported_keys['IP_keys'])
		packet_list.extend(to_extend)

		#gets IPv6 keys if they exist
		try:
			to_extend = []
			for x in range(0, len(self.supported_keys['IPv6_keys'])):
				to_extend.append(packet['IPv6'][self.supported_keys['IPv6_keys'][x]])
		except:
			to_extend = [0]*len(self.supported_keys['IPv6_keys'])
		packet_list.extend(to_extend)

		#gets ARP keys if they exist
		try:
			to_extend = []
			for x in range(0, len(self.supported_keys['ARP_keys'])):
				to_extend.append(packet['ARP'][self.supported_keys['ARP_keys'][x]])
		except:
			to_extend = [0]*len(self.supported_keys['ARP_keys'])
		packet_list.extend(to_extend)

		#gets LLDP keys if they exist
		try:
			to_extend = []
			for x in range(0, len(self.supported_keys['LLDP_keys'])):
				to_extend.append(packet['LLDP'][self.supported_keys['LLDP_keys'][x]])
		except:
			to_extend = [0]*len(self.supported_keys['LLDP_keys'])
		packet_list.extend(to_extend)

		#gets UDP keys if they exist
		try:
			to_extend = []
			for x in range(0, len(self.supported_keys['UDP_keys'])):
				to_extend.append(packet['packet_info'][self.supported_keys['UDP_keys'][x]])
		except:
			to_extend = [0]*len(self.supported_keys['UDP_keys'])
		packet_list.extend(to_extend)

		#gets TCP keys if they exist
		try:
			to_extend = []
			for x in range(0, len(self.supported_keys['TCP_keys'])):
				to_extend.append(packet['packet_info'][self.supported_keys['TCP_keys'][x]])
		except:
			to_extend = [0]*len(self.supported_keys['TCP_keys'])
		packet_list.extend(to_extend)

		#gets ICMP keys if they exist
		try:
			to_extend = []
			for x in range(0, len(self.supported_keys['ICMP_keys'])):
				to_extend.append(packet['packet_info'][self.supported_keys['ICMP_keys'][x]])
		except:
			to_extend = [0]*len(self.supported_keys['ICMP_keys'])
		packet_list.extend(to_extend)

		#gets IPv6 section keys if they exist
		try:
			to_extend = []
			for x in range(0, len(self.supported_keys['hop_by_hop_keys'])):
				to_extend.append(packet['packet_info'][self.supported_keys['hop_by_hop_keys'][x]])
		except:
			to_extend = [0]*len(self.supported_keys['hop_by_hop_keys'])
		packet_list.extend(to_extend)

		#gets IPv6 section keys if they exist
		try:
			to_extend = []
			for x in range(0, len(self.supported_keys['ICMPv6_keys'])):
				to_extend.append(packet['packet_info'][self.supported_keys['ICMPv6_keys'][x]])
		except:
			to_extend = [0]*len(self.supported_keys['ICMPv6_keys'])
		packet_list.extend(to_extend)

		#gets UDP section keys if they exist
		try:
			to_extend = []
			for x in range(0, len(self.supported_keys['NTP_keys'])):
				to_extend.append(packet['packet_info']['NTP'][self.supported_keys['NTP_keys'][x]])
		except:
			to_extend = [0]*len(self.supported_keys['NTP_keys'])
		packet_list.extend(to_extend)



		return packet_list



	#returns values from the Ethernet section of the packet
	def read_Ethernet_packet(self, packet_info, pkt):
		#intializes dictionary
		packet_info['Ethernet'] = {}
		packet_info['Ethernet']['overall_type'] = 0
		packet_info['Ethernet']['source'] = 0
		packet_info['Ethernet']['destination'] = 0
		packet_info['Ethernet']['timestamp'] = 0

		try:
			#get packet type (IP, ARP, etc.)
			packet_info['Ethernet']['overall_type'] = self.pkt_type[pkt.type]
			packet_info['Ethernet']['source'] = pkt.src
			packet_info['Ethernet']['destination'] = pkt.dst
			packet_info['Ethernet']['timestamp'] = pkt['Ethernet'].time
		except Exception as error:
			pkt.show()


	def read_LAN_packet(self, packet_info, pkt):
		packet_info['802.3'] = {}
		packet_info['802.3']['overall_type'] = self.pkt_type[pkt.type]
		packet_info['802.3']['source'] = pkt.src
		packet_info['802.3']['destination'] = pkt.dst






	def read_IP_packet(self, packet_info, pkt):
		packet_info['IP'] = {}

		#packet_type = 17 for UDP, 6 for TCP, 1 for ICMP
		IP_packet_type = self.IP_type[pkt[IP].proto]
		packet_info['IP']['packet_type'] = IP_packet_type
		#hexadecimal checksum is converted to decimal. 
		packet_info['IP']['checksum'] = pkt[IP].chksum
		packet_info['IP']['length'] = pkt[IP].len
		packet_info['IP']['source'] = pkt[IP].src
		packet_info['IP']['destination'] = pkt[IP].dst

		#if packet is of type UDP
		if IP_packet_type=="UDP":
			self.read_UDP_section(packet_info, pkt)
			# print("Time: "+str(pkt[UDP].time))

		#if packet is of type TCP
		elif IP_packet_type=="TCP": 
			self.read_TCP_section(packet_info, pkt)
			# print("Time: "+str(pkt[TCP].time))

		#if packet is of type ICMP
		elif IP_packet_type=="ICMP":
			self.read_ICMP_section(packet_info, pkt)
			# print("Time: "+str(pkt[ICMP].time))


	def read_ARP_packet(self, packet_info, pkt):
		#initializes dictionary
		packet_info['ARP'] = {}
		packet_info['ARP']['length'] = 0
		packet_info['ARP']['operation'] = 0
		packet_info['ARP']['hardware_source'] = 0
		packet_info['ARP']['protocol_source'] = 0
		packet_info['ARP']['hardware_destination'] = 0
		packet_info['ARP']['protocol_destination'] = 0

		try:
			packet_info['ARP']['length'] = pkt[ARP].plen
			packet_info['ARP']['operation'] = pkt[ARP].op
			packet_info['ARP']['hardware_source'] = pkt[ARP].hwsrc
			packet_info['ARP']['protocol_source'] = pkt[ARP].psrc
			packet_info['ARP']['hardware_destination'] = pkt[ARP].hwdst
			packet_info['ARP']['protocol_destination'] = pkt[ARP].pdst
		except Exception as error:
			# print("Couldn't read ARP packet: "+str(error))
			pass


	def read_IPv6_packet(self, packet_info, pkt):
		packet_info['IPv6'] = {}

		IPv6_packet_type = self.IP_type[pkt[IPv6].nh]
		packet_info['IPv6']['packet_type'] = IPv6_packet_type
		packet_info['IPv6']['traffic_class'] = pkt[IPv6].tc
		packet_info['IPv6']['payload_length'] = pkt[IPv6].plen
		packet_info['IPv6']['next_header'] = pkt[IPv6].nh
		packet_info['IPv6']['hop_limit'] = pkt[IPv6].hlim
		packet_info['IPv6']['source'] = pkt[IPv6].src
		packet_info['IPv6']['destination'] = pkt[IPv6].dst
		
		# packet_info['IPv6']['version'] = 
		# packet_info['IPv6']['version'] = 

		#if packet is of type Hop-by-Hop Option Header
		if IPv6_packet_type=="Hop-by-Hop Option Header": 
			pass

		#if packet is of type TCP
		elif IPv6_packet_type=="TCP": 
			self.read_TCP_section(packet_info, pkt)

		#if packet is of type UDP
		elif IPv6_packet_type=="UDP":
			self.read_UDP_section(packet_info, pkt)

		#if packet is of type ICMP
		elif IPv6_packet_type=="ICMP":
			input("ICMP packet type not yet supported...")

		elif IPv6_packet_type=="ICMPv6":
			self.read_ICMPv6_section(packet_info, pkt)

		else:
			print(IPv6_packet_type)
			input("Unrecognized IPv6 packet type...")




		# print("Next header: "+str(packet_info['IPv6']['next_header']))
		# print(packet_info)

	def read_LLDP_packet(self, packet_info, pkt):
		packet_info['LLDP'] = {}




	def read_UDP_section(self, packet_info, pkt):
		#initializes dictionary
		packet_info['packet_info'] = {}
		packet_info['packet_info']['source_port'] = 0
		packet_info['packet_info']['destination_port'] = 0
		packet_info['packet_info']['udp_len'] = 0
		packet_info['packet_info']['udp_checksum'] = 0

		try:
			packet_info['packet_info']['source_port'] = pkt[UDP].sport
			packet_info['packet_info']['destination_port'] = pkt[UDP].dport
			packet_info['packet_info']['udp_len'] = pkt[UDP].len
			packet_info['packet_info']['udp_checksum'] = pkt[UDP].chksum
		except Exception as error:
			# print("Couldn't read UDP section: "+str(error))
			pass


		#checks if this packet contains an NTP section
		is_NTP = False
		try:
			pkt['NTP']
			is_NTP = True
		except Exception as error:
			pass

		#NTP amplification is a type of DDoS attack
		if is_NTP:
			packet_info['packet_info']['NTP'] = {}
			packet_info['packet_info']['NTP']['leap'] = pkt['NTP'].leap
			packet_info['packet_info']['NTP']['mode'] = pkt['NTP'].mode
			packet_info['packet_info']['NTP']['stratum'] = pkt['NTP'].stratum
			packet_info['packet_info']['NTP']['dispersion'] = pkt['NTP'].dispersion
			packet_info['packet_info']['NTP']['id'] = pkt['NTP'].id


	def read_TCP_section(self, packet_info, pkt):
		#initializes dictionary
		packet_info['packet_info'] = {}
		packet_info['packet_info']['source_port'] = 0
		packet_info['packet_info']['destination_port'] = 0
		packet_info['packet_info']['ack'] = 0
		packet_info['packet_info']['flags'] = 0
		packet_info['packet_info']['tcp_checksum'] = 0
		packet_info['packet_info']['tcp_options'] = ""

		try:
			packet_info['packet_info']['source_port'] = pkt[TCP].sport
			packet_info['packet_info']['destination_port'] = pkt[TCP].dport
			packet_info['packet_info']['ack'] = pkt[TCP].ack
			packet_info['packet_info']['flags'] = pkt[TCP].flags
			packet_info['packet_info']['tcp_checksum'] = pkt[TCP].chksum
			packet_info['packet_info']['tcp_options'] = pkt[TCP].options
		except Exception as error:
			# print("Couldn't read TCP section: "+str(error))
			pass



	def read_ICMP_section(self, packet_info, pkt):
		#initializes dictionary
		packet_info['packet_info'] = {}
		packet_info['packet_info']['icmp_type'] = 0
		packet_info['packet_info']['icmp_checksum'] = 0

		try:
			packet_info['packet_info']['icmp_type'] = pkt[ICMP].type
			packet_info['packet_info']['icmp_checksum'] = pkt[ICMP].chksum
		except Exception as error:
			# print("Couldn't read ICMP section: "+str(error))
			pass


	def read_ICMPv6_section(self, packet_info, pkt):
		#initializes dictionary
		packet_info['packet_info'] = {}
		packet_info['packet_info']['icmp_type'] = 0
		packet_info['packet_info']['icmp_checksum'] = 0
		packet_info['packet_info']['target'] = 0

		try:

			packet_info['packet_info']['icmp_type'] = pkt['ICMPv6 Neighbor Discovery - Neighbor Solicitation'].type
			packet_info['packet_info']['icmp_checksum'] = pkt['ICMPv6 Neighbor Discovery - Neighbor Solicitation'].cksum
			packet_info['packet_info']['target'] = pkt['ICMPv6 Neighbor Discovery - Neighbor Solicitation'].tgt
		except:
			# print("Couldn't retrieve \"ICMPv6 Neighbor Discovery - Neighbor Solicitation\" information")
			pass




if __name__=="__main__":

	pcap_handler = PCAPHandler()

	test_path = "./Datasets/2018-10-31-traffic-analysis-exercise.pcap"
	pcap_handler.read_pcap(test_path)

	