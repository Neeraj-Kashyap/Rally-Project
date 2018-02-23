# Rally-Project
## An awesome car managed by vocal commands in rally slang
@barloccia coauthor

![Car image](https://github.com/adelmassimo/Rally-Project/blob/master/main.png)
Raspberry Pi based project, was born as a joke and grown up quickly and returned unexpected good results.

1. Find a structure and find out how manage engines with Raspberry: `main.py` is the routine.
2. Develop and improve offline speech-recognition, Snowboy used: `rpi/` and `osx/` contains the framework,
3. Develop a user interface for train models and manage the car: `app/`

## Snowboy speech recognition
Snowboy (https://snowboy.kitt.ai) is an highly customizable hotword detection engine that is embedded real-time and is always listening (even when offline) compatible with Raspberry Pi. For the purpose of recognize key words, snowboy use a trained models that can be improved by a community based strategy.

## User Interface
This interface was created with the purpose to manage raspberry by remote (see `app/synchronizer/` and `app/ssh_conn`)
and train snowboy models (see `app/train_routine`). The rest of code is stuff that put other stuff togheter.

![User Interface](https://github.com/adelmassimo/Rally-Project/blob/master/app.png)

To achieve above interface `PyQt5` were used, follows versions of requirements used:
Requirement | Version Used
------------ | -------------
Python | 3.6
PyQt | 5.10
pysftp | 0.2.9
PyAudio | 0.2.11
QDarkStyle | 2.3.1
