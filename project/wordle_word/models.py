from django.db import models
from django.utils import timezone
from random import sample
import csv

# Create your models here.


class Word(models.Model):
    word = models.CharField(unique=True, max_length=5)
    published_at = models.DateTimeField(null=True)

    def __str__(self) -> str:
        return self.word + " " + "published_at: " + str(self.published_at)

    @classmethod
    def todays_word(cls):
        current_time = timezone.now()
        last = Word.last_word()
        last_time = last.published_at
        diff = current_time - last_time

        # 60 second * 60 minutes * 24 hours
        # if diff.seconds < 60 * 60 * 24:
        # For easy testing, lower to 120 second
        if diff.seconds < 60:
            return last
        else:
            return Word.generate_word()

    @classmethod
    def generate_word(cls):
        all = Word.objects.filter(published_at__isnull=True)
        word = sample(list(all), 1)[0]
        Word.objects.filter(pk=word.id).update(published_at=timezone.now())
        return word

    @classmethod
    def last_word(cls):
        return Word.objects.order_by("-published_at")[0]

    # You will be fired if you use this!!!
    # But when you do use it, expect it to take some time
    @classmethod
    def dangerously_reset(cls):
        # Delete all records
        Word.objects.all().delete()
        # Seed database
        file = open("wordle_word/seed.csv")
        csvreader = csv.reader(file)
        for word in csvreader:
            entry = Word.objects.create(word=word[0].upper())
            entry.save()
        print("seeded DB")
