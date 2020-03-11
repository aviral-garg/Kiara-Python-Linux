from pyautogui import press, hotkey


def new_file(): ctrl('n')


def paste(): ctrl('v')


def enter(): press('enter')


def space(): press('space')


def ctrl(x): hotkey('ctrl', x)


def alt(x): hotkey('alt', x)


def shift(x):hotkey('shift', x)


def win(x): hotkey('win', x)