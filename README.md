# DDoS-Attack-Detection

Machine learning is used to detect whether a packet or packets are part of a DDoS attack. 

Currently, the model can only give a probability on a general DDoS attack. 

Required packages: 
* pip install kamene
* conda install keras
* conda install scikit-learn

Steps to add a new dataset: 
1) Create new directory in ./Datasets, with the name being anything you'd like. 
2) Add sequence of pcap files to the new directory
3) Add a .csv in ./Labels, which will have our labels. 
    * Each row in this csv will correspond to each packet in all of the pcap files.
	* Columns: 
	    * source
		* source_port
		* destination
		* destination_port
		* protocol
		* timestamp
		* label ("BENIGN" for non-DDoS packet, and "DDoS" for DDoS packet)
	* Example rows: 
	    * 172.16.0.1-192.168.10.50-33136-80-6,172.16.0.1,33136,192.168.10.50,80,6,5/7/2017 10:48,DoS Hulk
        * 192.168.10.14-216.58.219.226-51676-443-6,192.168.10.14,51676,216.58.219.226,443,6,5/7/2017 10:49,BENIGN
        * 172.16.0.1-192.168.10.50-33132-80-6,172.16.0.1,33132,192.168.10.50,80,6,5/7/2017 10:48,DoS Hulk
        * 172.217.12.161-192.168.10.14-443-51701-6,192.168.10.14,51701,172.217.12.161,443,6,5/7/2017 10:49,BENIGN
        * 172.217.12.164-192.168.10.14-443-51688-6,192.168.10.14,51688,172.217.12.164,443,6,5/7/2017 10:49,BENIGN
        * 172.16.0.1-192.168.10.50-33144-80-6,172.16.0.1,33144,192.168.10.50,80,6,5/7/2017 10:48,DoS Hulk
        * 172.16.0.1-192.168.10.50-33138-80-6,172.16.0.1,33138,192.168.10.50,80,6,5/7/2017 10:48,DoS Hulk
        * 172.16.0.1-192.168.10.50-33142-80-6,172.16.0.1,33142,192.168.10.50,80,6,5/7/2017 10:48,DoS Hulk
4) Run Main.py
5) Choose to calculate labels for new dataset.
