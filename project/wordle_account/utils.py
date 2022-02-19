import csv


def load_preface_list():
    file = open("wordle_account/seed.csv")
    csvreader = csv.reader(file)
    members = []
    for row in csvreader:
        members.append(row[0].lower())

    print("===== LOADING PREFACE LIST =====")
    return members
