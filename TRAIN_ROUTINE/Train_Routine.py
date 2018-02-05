import training_service as ts

#This script recall the train routine, defined in training_service.
#User have to spell three times the word with train the model when in output appear "PARLARE ORA!"
if __name__ == '__main__':
	
<<<<<<< HEAD
<<<<<<< HEAD:TRAIN_ROUTINE/Train_Routine.py
	ts.updateModel("right1", "trainingSamples/adel/", "../models/adel/")
=======
	ts.updateModel("ff", "../samples/", "../models/")
>>>>>>> 8a115b97fbd22d619d4359d6375b171efab035c5:rpi-arm-raspbian-8.0-1.1.1/TRAIN_ROUTINE/Train_Routine.py
=======
<<<<<<< HEAD:rpi-arm-raspbian-8.0-1.1.1/TRAIN_ROUTINE/Train_Routine.py
	ts.updateModel("ff", "../samples/", "../models/")
=======
	ts.updateModel("ff", "trainingSamples/", "../models/")
>>>>>>> 0416192c13468ec2eb022d4d98b548a950c01276:TRAIN_ROUTINE/Train_Routine.py
>>>>>>> 3b31edc41ef3937797e5a58a332f2b339ce40feb
	#FOR TEST ON MAC:
	#run ../osx-x86-64-1.1.1/demo.py or demo2.py
	#as you can see these scripts catch models in ../rpi.... folder