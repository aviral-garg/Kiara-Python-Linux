import speech_recognition as sr

WAIT_UNTIL_BOOL_ANSWER = None


def get_text_from_speech(_timeout=0.5):
    text = ''
    r = sr.Recognizer()
    with sr.Microphone() as audio_source:
        # recognize speech using Google Speech Recognition
        try:
            audio = r.listen(audio_source, timeout=_timeout)
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            text = r.recognize_google(audio)
            print(f'Avi : {text}')
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

        except sr.WaitTimeoutError:
            # print('DEBUG: speechrecognition.WaitTimeoutError')
            pass

    return text


def str_to_bool_char(_str):
    return "n" if "no" in _str else "y"


def get_voice_input(bool_answer=False):
    _s = get_text_from_speech(_timeout=WAIT_UNTIL_BOOL_ANSWER)
    _s = str_to_bool_char(_s) if bool_answer else _s
    return _s
