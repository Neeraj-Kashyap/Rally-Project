import training_service as ts

#This script recall the train routine, defined in training_service.
#User have to spell three times the word with train the model when in output appear "PARLARE ORA!"
if __name__ == '__main__':
	
<<<<<<< HEAD:TRAIN_ROUTINE/Train_Routine.py
	ts.updateModel("right1", "trainingSamples/adel/", "../models/adel/")
=======
	ts.updateModel("ff", "../samples/", "../models/")
>>>>>>> 8a115b97fbd22d619d4359d6375b171efab035c5:rpi-arm-raspbian-8.0-1.1.1/TRAIN_ROUTINE/Train_Routine.py
	#FOR TEST ON MAC:
	#run ../osx-x86-64-1.1.1/demo.py or demo2.py
	#as you can see these scripts catch models in ../rpi.... folder