from datetime import timezone
from django.conf import settings
from django.db import models
from django.utils import timezone
from wordle_word.models import Word

# Create your models here.


class Game(models.Model):
    player = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    won = models.BooleanField(null=True)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    # 5 letters word * 6 tries + 5 commas = 35
    attempts = models.CharField(blank=True, max_length=35)
    created_date = models.DateTimeField(default=timezone.now)

    def start_game(self, request):
        word = Word.todays_word()
        return Game.objects.create(
            player=request.user,
            word=word,
        )

    def attempt(self, request):
        pass
