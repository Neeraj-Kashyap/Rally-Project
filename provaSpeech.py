import time, pyglet, timeit
import speech_recognition as sr


bg_sound_path = 'sounds/bg_sound.wav'

# this is called from the background thread
def heardSomething(recognizer, audio):
    # received audio data, now we'll recognize it using Google Speech Recognition
    start = timeit.default_timer()
    try:

        message = recognizer.recognize_wit(audio, key="YCTWXXXALS7JKLZMD6LIMYYBB5UHDA6F", show_all=False)
        stop = timeit.default_timer()
        totalTime = str( stop - start )
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        out_file = open("log.txt","a")
        out_file.write(message +" time:"+ totalTime +"\n")
        out_file.close()
        print("Ricevuto: " + message)

        if "sinistra" in message:
            print ("Do something sx")
        elif "destra" in message:
            print ("Do something dx")
    
    except sr.UnknownValueError:
        print("Non ho sentito bene!")
    except sr.RequestError as e:
        print("error: Could not request results from Google Speech Recognition service; {0}".format(e))


def playSound(paht_to_sound, is_loop):
    snd = pyglet.media.load(paht_to_sound)
    looper = pyglet.media.SourceGroup(snd.audio_format, None)
    looper.loop = is_loop
    looper.queue(snd)
    p = pyglet.media.Player()
    p.queue(looper)
    p.play()
    pyglet.app.run()

r = sr.Recognizer()
m = sr.Microphone()

#print(m)
with m as source:
    r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening

print("start speaking")
# start listening in the background (note that we don't have to do this inside a `with` statement)
r.listen_in_background(m, heardSomething)

while True:
    time.sleep(5)
    
#playSound(bg_sound_path, False)







# while True: time.sleep(0.1)
# `stop_listening` is now a function that, when called, stops background listening

# # do some unrelated computations for 5 seconds
# for _ in range(50): time.sleep(0.1)  # we're still listening even though the main thread is doing other things

# # calling this function requests that the background listener stop listening
# stop_listening()

# # do some more unrelated things
# while True: time.sleep(0.1)  # we're not listening anymore, even though the background thread might still be running for a second or two while cleaning up and stopping
