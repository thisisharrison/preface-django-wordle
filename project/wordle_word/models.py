from datetime import timedelta
import pdb
from django.db import models
from django.utils import timezone, formats
from random import shuffle
import csv


# Create your models here.


class Word(models.Model):
    word = models.CharField(unique=True, max_length=5)
    published_at = models.DateField(null=True)

    def __str__(self) -> str:
        return f"{self.word} {formats.date_format(self.published_at) if self.published_at else ''}"

    @classmethod
    def todays_word(cls):
        today = timezone.localdate()
        word = Word.objects.get(published_at__exact=today)
        return word

    @classmethod
    def valid_word(cls, word):
        try:
            obj = Word.objects.get(word__exact=word)
        except Word.DoesNotExist:
            obj = None
        return obj

    # You will be fired if you use this!!!
    # But when you do use it, expect it to take some time
    @classmethod
    def dangerously_reset(cls):
        # Delete all records
        Word.objects.all().delete()

        # Seed database
        file = open("wordle_word/seed.csv")
        csvreader = csv.reader(file)

        # To shuffle save words to list first
        words = []
        for row in csvreader:
            words.append(row[0].upper())

        shuffle(words)

        # Get today's date and increment by 1
        start_date = timezone.localdate()
        for i, word in enumerate(words):
            published_date = start_date + timedelta(days=i)
            entry = Word.objects.create(word=word, published_at=published_date)
            entry.save()

        print("seeded DB")
