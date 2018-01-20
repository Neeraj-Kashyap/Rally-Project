import snowboydecoder
import sys
import signal

interrupted = False


def signal_handler(signal, frame):
    global interrupted
    interrupted = True

def culo():
	print("beccato")

def interrupt_callback():
    global interrupted
    return interrupted

model = "../rpi-arm-raspbian-8.0-1.1.1/models/micio.pmdl"


# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

detector = snowboydecoder.HotwordDetector(model, sensitivity=.5)
print('Listening... Press Ctrl+C to exit')

# main loop
detector.start(detected_callback=culo,
               interrupt_check=interrupt_callback,
               sleep_time=0.001)

detector.terminate()
