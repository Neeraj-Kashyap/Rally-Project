import pyaudio
import wave
import sys

def records(output, seconds):
	print("Paralere ora")

	
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