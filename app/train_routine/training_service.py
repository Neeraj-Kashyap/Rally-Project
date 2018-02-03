import sys  
import base64
import requests
import pickle
import pyaudio
import wave


def get_wave(fname):
    with open(fname) as f:
        infile = pickle.load(f, encoding='utf32') 
        return base64.b64encode(infile.read())

endpoint = "https://snowboy.kitt.ai/api/v1/train/"
############# MODIFY THE FOLLOWING #############
token = "349034c5564b53f3f16aac324f112ff9125c6733"
hotword_name = "sinistra"
language = "it"
age_group = "20_29"
gender = "M"
microphone = "headset microphone"
############### END OF MODIFY ##################

#This function record for some seconds (default 2) a wav file, named "modelX.wav", and save it in samples_path directory.
#After file were recorded and stored, a same-named model is ponted in the models_path directory.
#Three registrations and model are sent via HTTP to the server, that update and override the model with respect to the audiofiles.
def updateModel(model, samples_path = "samples/", models_path = "../models/", recTime = 2):
    #record and store.
    #note that function record in defined in helper.py
    wav1 = records(samples_path+model+"1.wav", recTime)

    wav2 = records(samples_path+model+"2.wav", recTime)
    
    wav3 = records(samples_path+model+"3.wav", recTime)
    # wav1 = '../samples/right11.wav'
    # wav2 = '../samples/right12.wav'
    # wav3 = '../samples/right13.wav'
    # #pick model
    out = models_path+model+".pmdl"
    #From below some seconds needed: uploading + computing + responding
    print("now i'm having workout")
    data = {
        "name": model,
        "language": language,
        "age_group": age_group,
        "gender": gender,
        "microphone": microphone,
        "token": token,
        "voice_samples": [
            {"wave": get_wave(wav1)},
            {"wave": get_wave(wav2)},
            {"wave": get_wave(wav3)}
        ]
    }

    response = requests.post(endpoint, json=data)
    if response.ok:
        with open(out, "w") as outfile:
            outfile.write(response.content)
        print("Saved model to '%s'." % out)
    else:
        print ("Request failed.")
        print (response.text)










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