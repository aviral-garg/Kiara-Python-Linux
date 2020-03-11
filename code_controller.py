from pyautogui import press
from xerox import copy

from helper import paste, enter


def code_ctrlr(_first_word=None, words=None, _sentence=None):
    if not _first_word or not words or not _sentence:
        raise ValueError("_first_word and _sentence can't None")

    _first_word = _first_word.lower()

    # todo: content awareness (knowing what variable names have just been used)
    #       => higher priority to LRU variable names

    if _first_word == "if":
        op, op1, op2 = "", "", ""

        if "in" in words:
            op1 = "is" if "is" in words else "in"  # todo: improve this
            op2 = "in"
            op = "in"
        elif "equals" in words:
            if "is" in words:  # todo: improve this
                op1 = "is"
            elif "equal" in words:
                op1 = "equal"
            elif "equals" in words:
                op1 = "equals"
            op = "=="
        elif "less than equal" in _sentence:
            op1 = "is" if "is" in words else "less"  # todo: improve this
            op2 = "to"
            op = "<="
        elif "greater than equal" in _sentence:
            op1 = "is" if "is" in words else "greater"  # todo: improve this
            op2 = "to"
            op = ">="
        elif "greater than" in _sentence:
            op1 = "is" if "is" in words else "greater"  # todo: improve this
            op2 = "than"
            op = ">"
        elif "less than" in _sentence:
            op1 = "is" if "is" in words else "less"  # todo: improve this
            op2 = "than"
            op = "<"

        operand1_end = words.index(op1)
        operand2_start = words.index(op2) + 1

        operand_1 = "_".join(words[1:operand1_end])
        operand_2 = "_".join(words[operand2_start:])

        text = f"if {operand_1} {op} {operand_2}:"
        copy(text)
        paste()
        enter()

    elif "equals" in words or "equal" in words:
        operand_1 = "_".join(words[1:operand1_end])
        operand_2 = "_".join(words[operand2_start:])
        op = "=="
        text = f"if {operand_1} {op} {operand_2}:"
        copy(text)
        paste()
        enter()

    elif _first_word == "print":
        text = "print"
        copy(text)
        paste()
        press('(')

    elif _first_word == "return":
        text = ""
        if words[1].lower() in ["true", "false"]:
            text = f"return {words[1][0].upper() + words[1][1:]}"
        else:
            text = _sentence
        copy(text)
        paste()
        return True

    elif _first_word == "raise":
        if "implemented" in words:
            copy("raise NotImplementedError('To be Implemented')")
            paste()
            return True
        else:
            print("didn't recognise the error to raise")
            return False

    elif _first_word == "for":
        text = ""
        if "range" in words:
            iterator_name = words[1] if len(words) > 1 else None
            if "to" in words:
                to_i = words.index("to")
                start = words[to_i - 1]
                end = words[to_i + 1]
                text = f"for {iterator_name} in range({start}, {end}):"
            else:
                range_i = words.index("range")
                if range_i + 1 < len(words):
                    end = words[range_i + 1]
                    text = f"for {iterator_name} in range({end}):"
                else:
                    print("please mention the range-end for the loop")
                    return False
        copy(text)
        paste()
        enter()
        return True
