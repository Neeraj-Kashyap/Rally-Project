import sys
import base64
import requests
import helper

def get_wave(fname):
    with open(fname) as infile:
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
    wav1 = helper.records(samples_path+model+"1.wav", recTime)

    wav2 = helper.records(samples_path+model+"2.wav", recTime)
    
    wav3 = helper.records(samples_path+model+"3.wav", recTime)
    #pick model
    out = models_path+model+".pmdl"
    #From below some seconds needed: uploading + computing + responding
    print("now i'm having workout")
    data = {
        "name": hotword_name,
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