import pyaudio
import pygame
import pyaudio
import wave
import sys

<<<<<<< HEAD:rpi-arm-raspbian-8.0-1.1.1/TRAIN_ROUTINE/helper.py
def playSound():
	chunk = 1024
	# open the file for reading.
	wf = wave.open('../../sounds/training.wav', 'rb')

	# create an audio object
	p = pyaudio.PyAudio()

	# open stream based on the wave object which has been input.
	stream_ = p.open(format =
                p.get_format_from_width(wf.getsampwidth()),
                channels = wf.getnchannels(),
                rate = wf.getframerate(),
                output = True)

	# read data (based on the chunk size)
	data = wf.readframes(chunk)

	# play stream (looping from beginning of file to the end)
	while data != '':
		stream_.write(data)
		data = wf.readframes(chunk)
	
	# cleanup stuff.
	stream_.close()    
	p.terminate()



=======
>>>>>>> 0416192c13468ec2eb022d4d98b548a950c01276:TRAIN_ROUTINE/helper.py
def records(output, seconds):
	print("AUDIO SIGNAL")
	playSound()
	#print("PARLARE ORA!")

	
	FORMAT = pyaudio.paInt16
	CHANNELS = 1
	RATE = 44100
	CHUNK = 1024
	RECORD_SECONDS = seconds
	WAVE_OUTPUT_FILENAME = output

	audio = pyaudio.PyAudio()

	# start recording
	stream = audio.open(format=FORMAT, channels=CHANNELS,
					rate=RATE, input=True,
					frames_per_buffer=CHUNK)

	
	
	frames = []
	 
	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
	    data = stream.read(CHUNK)
	    frames.append(data)
	print ("finished recording")

	# stop Recording
	stream.stop_stream()
	stream.close()
	audio.terminate()
	 
	waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
	waveFile.setnchannels(CHANNELS)
	waveFile.setsampwidth(audio.get_sample_size(FORMAT))
	waveFile.setframerate(RATE)
	waveFile.writeframes(b''.join(frames))
	waveFile.close()
	return output