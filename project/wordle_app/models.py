from datetime import timezone
from django.conf import settings
from django.db import models
from django.utils import timezone, formats
from django.core.validators import MinValueValidator, MaxValueValidator
from wordle_word.models import Word
from .utils import is_same_date
import pdb

# Create your models here.


class Game(models.Model):
    player = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="games", on_delete=models.CASCADE
    )
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    attempts = models.CharField(blank=True, max_length=35)
    tries = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(6)]
    )
    won = models.BooleanField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Game Detail view
    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("wordle_app:game", kwargs={"pk": self.pk})

    def is_valid(self):
        diff = timezone.localdate() - self.created_at.date()
        if diff.days > 0:
            return False
        return True

    @classmethod
    def start_new_game(cls, request):
        word = Word.todays_word()
        return Game.objects.create(
            player=request.user,
            word=word,
        )

    def __str__(self) -> str:
        return f"{self.player.username} | {self.word} | {self.attempts} | {self.won} | ({formats.date_format(self.created_at, 'SHORT_DATE_FORMAT') if self.created_at else ''})"
