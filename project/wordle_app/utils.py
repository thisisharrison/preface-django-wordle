from functools import reduce
from collections import OrderedDict
import pdb


def word_to_word_dict(word):
    word_dict = {}
    for i, char in enumerate(word):
        word_dict[i] = char
    return word_dict


def attempts_to_list(attempts, word, word_dict):
    attempts_list = []
    attempts = list(map(lambda word: list(word), attempts.split(",")))

    if len(attempts[0]) == 0:
        return attempts_list

    for attempt in attempts:
        row = []
        for i, char in enumerate(attempt):
            if char is word_dict[i]:
                row.append((char, "correct"))
            elif char in word:
                row.append((char, "present"))
            else:
                row.append((char, "absent"))
        attempts_list.append(row)
    return attempts_list


def attempts_to_unique_dict(attempts_list):
    order = {"absent": 0, "present": 1, "correct": 2}

    def add_to_dict(summary, word):
        for char, state in word:
            if char in summary and order[state] > order[summary[char]]:
                summary[char] = state
            elif char not in summary:
                summary[char] = state
        return summary

    return reduce(add_to_dict, attempts_list, {})


def keyboard_to_list(unique_dict):
    KEYBOARD = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
    keyboard_list = []

    for row in KEYBOARD:
        row_dict = OrderedDict()
        for char in row:
            row_dict[char] = unique_dict[char] if char in unique_dict else ""
        keyboard_list.append(dict(row_dict))

    return keyboard_list


def transform_data(word, attempts):
    word_dict = word_to_word_dict(word)
    attempts_list = attempts_to_list(attempts, word, word_dict)
    unique_dict = attempts_to_unique_dict(attempts_list)
    keyboard_list = keyboard_to_list(unique_dict)
    return [attempts_list, keyboard_list]
