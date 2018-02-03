import training_service as ts

#This script recall the train routine, defined in training_service.
#User have to spell three times the word with train the model when in output appear "PARLARE ORA!"
if __name__ == '__main__':
	
<<<<<<< HEAD:rpi-arm-raspbian-8.0-1.1.1/TRAIN_ROUTINE/Train_Routine.py
	ts.updateModel("ff", "../samples/", "../models/")
=======
	ts.updateModel("ff", "trainingSamples/", "../models/")
>>>>>>> 0416192c13468ec2eb022d4d98b548a950c01276:TRAIN_ROUTINE/Train_Routine.py
	#FOR TEST ON MAC:
	#run ../osx-x86-64-1.1.1/demo.py or demo2.py
	#as you can see these scripts catch models in ../rpi.... folder