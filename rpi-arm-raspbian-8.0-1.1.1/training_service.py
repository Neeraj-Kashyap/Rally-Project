import sys
import base64
import requests
import helper as rec

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

samples_path = "samples/"
models_path = "models/"
############### END OF MODIFY ##################

def updateModel(model, recTime = 2):

    wav1 = rec.records(samples_path+model+"1.wav", recTime)
    wav2 = rec.records(samples_path+model+"2.wav", recTime)
    wav3 = rec.records(samples_path+model+"3.wav", recTime)
    out = models_path+model+".pmdl"

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
        print "Saved model to '%s'." % out
    else:
        print "Request failed."
        print response.text