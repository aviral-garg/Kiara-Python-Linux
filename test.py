# !/usr/bin/env python3
from queue import Queue  # Python 3 import
from threading import Thread

import speech_recognition as sr

from code_controller import code_ctrlr
from helper import paste, shift

r = sr.Recognizer()
audio_queue = Queue()

STOP_LISTENING_HOTWORDS = {'stop listening', 'bye'}


def rerun(py_charm=True):  # TODO: increase support + ability to bring correct window to focus
    if py_charm:
        shift("f10")
        return True
    return False


def other_cmds_ctrlr(_first_word, words, sentence):
    if _first_word == "paste":
        paste()
        return True
    if _first_word in ["run", "rerun"]:
        rerun()
        return True
    return False


def features_controller(sentence, words):
    # search_ctrlr(words[0])
    # type_ctrlr(words[0], sentence)
    # keyboard_cmd_ctrlr(words[0], words, sentence)
    if code_ctrlr(words[0], words, sentence):
        return True
    if other_cmds_ctrlr(words[0], words, sentence):
        return True


def cmd_dispatcher(sentence):
    if sentence in STOP_LISTENING_HOTWORDS:
        return True

    # setup
    sentence = str.lower(sentence)
    words = sentence.split(' ')

    features_controller(sentence, words)


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
                sentence = r.recognize_google(audio)
                print("Avi: " + sentence)
                cmd_dispatcher(sentence)
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
                audio_queue.put(r.listen(source, timeout=1))
            except sr.WaitTimeoutError:
                # print('DEBUG: speechrecognition.WaitTimeoutError')
                print(".")
                pass
    except KeyboardInterrupt:  # allow Ctrl + C to shut down the program
        pass

audio_queue.join()  # block until all current audio processing jobs are done
audio_queue.put(None)  # tell the recognize_thread to stop
recognize_thread.join()  # wait for the recognize_thread to actually stop
