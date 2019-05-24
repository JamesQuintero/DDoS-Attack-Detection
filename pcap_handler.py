from kamene.all import * #library used to read pcap fils



class PCAPHandler:

	def __init__(self):
		pass

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


		for pkt in packets:
			# print(pkt.show())

			print(pkt[IP].dst)

			input()

		for x in range(0, len(packets)):
			# print(packets[x])
			pkt = packets[x]

			# #prints packets in hex format
			# print(hexdump(pkt))

			#prints the bytes version of the already byte default packet
			# print(bytes(pkt))

			print(Ether(pkt))



			input()

		print("Num packets: "+str(len(packets)))


if __name__=="__main__":

	pcap_handler = PCAPHandler()

	test_path = "./Dataset/2018-10-31-traffic-analysis-exercise.pcap"
	pcap_handler.read_pcap(test_path)