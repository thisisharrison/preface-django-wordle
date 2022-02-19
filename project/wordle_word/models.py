from datetime import timedelta
from django.db import models
from django.utils import timezone, formats
from random import shuffle
import pdb

from .utils import load_word_list


# Create your models here.


class Word(models.Model):
    word = models.CharField(unique=True, max_length=5)
    published_at = models.DateField(null=True)

    _word_list = load_word_list()

    def __str__(self) -> str:
        return f"{self.word} ({formats.date_format(self.published_at, 'SHORT_DATE_FORMAT') if self.published_at else ''})"

    # TODO: Use redis or other cache to optimize in the future
    @classmethod
    def valid_word(cls, word):
        return word in cls._word_list

    @staticmethod
    def todays_word():
        today = timezone.localdate()
        word = Word.objects.get(published_at__exact=today)
        return word

    # You will be fired if you use this!!!
    @staticmethod
    def dangerously_reset():
        # Delete all records
        Word.objects.all().delete()

        words = load_word_list()
        shuffle(words)

        # Get today's date and increment by 1
        entries = []
        start_date = timezone.localdate()
        for i, word in enumerate(words[:10]):
            published_date = start_date + timedelta(days=i)
            entry = Word(word=word, published_at=published_date)
            entries.append(entry)

        Word.objects.bulk_create(entries)
        print("seeded DB")
