import training_service as ts

#This script recall the train routine, defined in training_service.
#User have to spell three times the word with train the model when in output appear "PARLARE ORA!"
if __name__ == '__main__':
	
	ts.updateModel("right3", "../samples/", "../models/")

	#FOR TEST ON MAC:
	#run ../osx-x86-64-1.1.1/demo.py or demo2.py
	#as you can see these scripts catch models in ../rpi.... folder