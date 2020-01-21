# import speech_recognition as sr
#
# r = sr.Recognizer()
# m = sr.Microphone()
# TIMEOUT = 0.5
#
# try:
#     print("A moment of silence, please...")
#     with m as source:
#         r.adjust_for_ambient_noise(source)
#     print("Set minimum energy threshold to {}".format(r.energy_threshold))
#     while True:
#         try:
#             with m as source:
#                 audio = r.listen(source, timeout=TIMEOUT)
#         try:
#
#             # recognize speech using Google Speech Recognition
#             value = r.recognize_google(audio)
#
#             # we need some special handling here to correctly print unicode characters to standard output
#             if str is bytes:  # this version of Python uses bytes for strings (Python 2)
#                 print(u"You said {}".format(value).encode("utf-8"))
#             else:  # this version of Python uses unicode for strings (Python 3+)
#                 print("You said {}".format(value))
#         except sr.UnknownValueError:
#             print("Oops! Didn't catch that")
#         except sr.RequestError as e:
#             print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
#         except sr.WaitTimeoutError:
#             # print('DEBUG: speechrecognition.WaitTimeoutError')
#             pass
# except KeyboardInterrupt:
#     pass


# !/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

from queue import Queue  # Python 3 import
from threading import Thread

import speech_recognition as sr

from text_to_speech import say

r = sr.Recognizer()
audio_queue = Queue()


def recognize_worker(use_google=True):
    # this runs in a background thread
    while True:
        audio = audio_queue.get()  # retrieve the next audio processing job from the main thread
        if audio is None:
            break  # stop processing if the main thread is done

        if use_google:

            # received audio data, now we'll recognize it using Google Speech Recognition
            try:
                # for testing purposes, we're just using the default API key
                # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
                # instead of `r.recognize_google(audio)`
                print("Avi: " + r.recognize_google(audio))
                say("I don't shit a fuck!")
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
        else:
            # received audio data, now we'll recognize it using Sphinx
            try:
                print("Avi: " + r.recognize_sphinx(audio))
            except sr.UnknownValueError:
                print("Sphinx could not understand audio")
            except sr.RequestError as e:
                print("Sphinx error; {0}".format(e))

        audio_queue.task_done()  # mark the audio processing job as completed in the queue


# start a new thread to recognize audio, while this thread focuses on listening
recognize_thread = Thread(target=recognize_worker)
recognize_thread.daemon = True
recognize_thread.start()
with sr.Microphone() as source:
    try:
        print("A moment of silence, please...")
        r.adjust_for_ambient_noise(source)
        print("Set minimum energy threshold to {}".format(r.energy_threshold))

        while True:  # repeatedly listen for phrases and put the resulting audio on the audio processing job queue
            try:
                audio_queue.put(r.listen(source, timeout=0.5))
            except sr.WaitTimeoutError:
                # print('DEBUG: speechrecognition.WaitTimeoutError')
                pass
    except KeyboardInterrupt:  # allow Ctrl + C to shut down the program
        pass

audio_queue.join()  # block until all current audio processing jobs are done
audio_queue.put(None)  # tell the recognize_thread to stop
recognize_thread.join()  # wait for the recognize_thread to actually stop
