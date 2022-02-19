import os
import csv

DIR = os.path.dirname(os.path.realpath(__file__))


def load_word_list():
    file = open(os.path.join(DIR, "seed.csv"))
    csvreader = csv.reader(file)
    words = []
    for row in csvreader:
        words.append(row[0])

    print("===== LOADING WORD LIST =====")
    return words
