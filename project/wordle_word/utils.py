import csv


def load_word_list():
    file = open("wordle_word/seed.csv")
    csvreader = csv.reader(file)
    words = []
    for row in csvreader:
        words.append(row[0])

    print("===== LOADING WORD LIST =====")
    return words
