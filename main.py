from pyperclip import copy, paste

from speech_to_text import get_text_from_speech
from text_to_speech import say

STOP_LISTENING_HOTWORDS = {'stop listening', 'bye'}


def code_ctrlr(_first_word=None, words=None, _sentence=None):
    if not _first_word or not _sentence:
        raise ValueError("_first_word and _sentence can't None")

    if _first_word.lower() == "raise":
        if "implemented" in words:
            copy(_sentence)
            paste()
        else:
            print("didn't recognixe the error to raise")


def features_controller(sentence, words):
    print(sentence, words)

    # search_ctrlr(words[0])
    # type_ctrlr(words[0], sentence)
    # keyboard_cmd_ctrlr(words[0], words, sentence)
    code_ctrlr(words[0], sentence)


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
