from speech_to_text import get_text_from_speech
from text_to_speech import say

STOP_LISTENING_HOTWORDS = {'stop listening', 'bye'}


def features_controller(sentence, words):
    print(sentence, words)


def cmd_dispatcher(sentence):
    if sentence in STOP_LISTENING_HOTWORDS:
        return True

    # setup
    sentence = str.lower(sentence)
    words = sentence.split(' ')

    features_controller(sentence, words)


def init():
    # starting with speech searches
    # cmd_dispatcher("testing")
    pass


def controller():
    init()

    while True:
        if cmd_dispatcher(get_text_from_speech()):
            break


if __name__ == '__main__':
    say(f'Kiara is alive')
    controller()
