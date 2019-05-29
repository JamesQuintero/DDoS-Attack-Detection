## James Quintero
## https://github.com/JamesQuintero
## Created: 5/2019
## Modified: 5/2019
##
## Handles all the data required for the program


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
        print("0) Quit")

        choice = int(input("Choice: "))

        #train model
        if choice==1:
            print("Chose to train a model")
            pass

        #test model on dataset
        elif choice==2:
            self.test_model()

        #Run model on live packets
        elif choice==3:
            print("Chose to run the model on live packets")
            pass

        #Quits the program
        elif choice==0:
            return False


        return True


    #menu choice to train a model
    def train_model(self):
        pass



    #menu choice to test a model
    def test_model(self):

        self.data_handler.print_dataset_list()
        
        choice = int(input("Dataset choice: "))

        print("Choice: "+str(self.data_handler.get_dataset_path(choice)))


        self.DDoS_detector.test(choice)



    #menu choice to run the model on live packets
    def run_model(self):
        pass



if __name__=="__main__":
    main = Main()

    success = True
    while success:
        success = main.menu()
