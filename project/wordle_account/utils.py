import os
import csv

DIR = os.path.dirname(os.path.realpath(__file__))


def load_preface_list():
    file = open(os.path.join(DIR, "seed.csv"))
    csvreader = csv.reader(file)
    members = []
    for row in csvreader:
        members.append(row[0].lower())

    print("===== LOADING PREFACE LIST =====")
    return members
