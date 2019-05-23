from kamene.all import * #library used to read pcap fils



class PCAPHandler:

	def __init__(self):
		pass

	def read_pcap(self, path):

		packets = []
		# with kamene.PcapReader(path) as pcap_reader:
		# 	for pkt in pcap_reader:
		# 		#do something with the packet
		# 		packets.append(pkt)


		pkts = rdpcap(path)

		print("Num packets: "+str(len(pkts)))


if __name__=="__main__":

	pcap_handler = PCAPHandler()

	test_path = "./Dataset/2018-10-31-traffic-analysis-exercise.pcap"
	pcap_handler.read_pcap(test_path)