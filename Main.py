## James Quintero
## https://github.com/JamesQuintero
## Created: 5/2019
## Modified: 4/2021
##
## Handles all the data required for the program


import os
from os import listdir
from os.path import isfile, join


from data_handler import DataHandler
from DDoS_detector import DDoSDetector



class Main():


    #DataHandler object 
    data_handler = None

    #DDoSDetector object
    DDoS_detector = None



    def __init__(self):
        self.data_handler = DataHandler()
        self.DDoS_detector = DDoSDetector()


    #gives the user a menu
    def menu(self):

        print("1) Train Model")
        print("2) Test model on dataset")
        print("3) Run model on live packets")
        print("4) Calculate labels for new dataset")
        print("0) Quit")

        choice = int(input("Choice: "))
        print()

        #train model
        if choice==1:
            self.train_menu()

        #test model on dataset
        elif choice==2:
            self.test_model()

        #Run model on live packets
        elif choice==3:
            self.run_live_menu()

        elif choice==4:
            self.calculate_labels_menu()

        #Quits the program
        elif choice==0:
            return False


        return True


    #menu choice to train a model
    def train_menu(self):
        choice = self.get_dataset_index_choice()

        self.DDoS_detector.train(dataset_index=choice, pcap_index=None)


    #menu choice to test a model
    def test_model(self):
        choice = self.get_dataset_index_choice()

        self.DDoS_detector.predict(choice)



    #menu choice to run the model on live packets
    def run_live_menu(self):
        print("Specify the model to use for predicting DDoS attacks on live packet sniffing")

        choice = self.get_dataset_index_choice()

        self.DDoS_detector.predict_live(dataset_index=choice)


    #menu choice to calculate labels for a new dataset
    def calculate_labels_menu(self):
        print("New dataset pcap files should already be in a new directory in ./Datasets/, and a csv file with the same dataset name should be in ./Labels/, with the last column of that csv being the actual labels. ")

        choice = self.get_dataset_index_choice()

        self.data_handler.calculate_labels(choice)

    #returns int corresponding to the dataset in ./Datasets
    def get_dataset_index_choice(self):
        self.print_dataset_list()
        
        choice = int(input("Dataset choice: "))
        print("Choice: "+str(self.data_handler.get_dataset_path(choice)))
        print()

        return choice

    #prints list of datasets
    def print_dataset_list(self):
        base_path = "./Datasets"

        dataset_dirs = self.data_handler.datasets

        #Gets datasets available for training
        num_dataset_files = []
        for folder in dataset_dirs:
            folder_path = base_path+"/"+folder

            dataset_files = os.listdir(folder_path)
            pcap_files = [ file for file in dataset_files if ".pcap" in file ]
            num_dataset_files.append(len(pcap_files))

        print("Datasets available: ")
        for x in range(0, len(dataset_dirs)):
            print("{}) {} ({} pcap files)".format(x, dataset_dirs[x], num_dataset_files[x]))



if __name__=="__main__":
    main = Main()

    success = True
    while success:
        success = main.menu()
