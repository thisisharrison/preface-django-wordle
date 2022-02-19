from functools import reduce
from collections import OrderedDict
from datetime import datetime, timedelta
from django.utils import timezone
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


def keyboard_to_list(unique_dict={}):
    KEYBOARD = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]
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


def next_game_time():
    curr_date = timezone.localdate()
    curr_time = timezone.localtime()

    next_date = curr_date + timedelta(days=1)
    next_time = datetime(
        next_date.year, next_date.month, next_date.day, tzinfo=curr_time.tzinfo
    )
    return [curr_date, next_time - curr_time]


def is_same_date(date1, date2):
    date1 = timezone.localtime(date1)
    return (
        date1.year == date2.year and date1.month == date2.month and date1.day == date2.day
    )
