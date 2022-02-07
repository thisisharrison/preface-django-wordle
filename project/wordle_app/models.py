from datetime import timezone
from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.core.validators import MinValueValidator, MaxValueValidator
from wordle_word.models import Word
import pdb

# Create your models here.


class Game(models.Model):
    player = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    # 5 letters word * 6 tries + 5 commas = 35
    attempts = models.CharField(blank=True, max_length=35)
    # 6 tries
    tries = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(6)]
    )
    won = models.BooleanField(null=True)
    created_at = models.DateTimeField(default=timezone.now)
    # Adding this to your DateTime field will add a timestamp as soon as the record is created as well as when the record is updated.
    updated_at = models.DateTimeField(auto_now=True)

    # Game Detail view
    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("wordle_app:game", kwargs={"pk": self.pk})

    def is_valid(self):
        diff = self.created_at.date() - timezone.localdate()
        if diff.days > 0:
            return False
        return True

    @classmethod
    def start_game(cls, request):
        word = Word.todays_word()
        return Game.objects.create(
            player=request.user,
            word=word,
        )

    def attempt(self, request):
        # TODO
        pdb.set_trace()
        pass

    def __str__(self) -> str:
        return f"{self.player}: {self.word}: {self.attempts}"
