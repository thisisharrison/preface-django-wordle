from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings

# Create your models here.

# TODO: replace calculations in view to use DB instead
class Statistic(models.Model):
    player = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # 023789 -> 1st try: 0, 2nd try: 2, etc.
    distribution = models.CharField(blank=True, max_length=6)
    played = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    current_streak = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(0)]
    )
    max_streak = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])

    @classmethod
    def add_stats(cls):
        pass

    def __str__(self):
        return f"{self.player.username} | {self.distribution} | {self.played} | {self.current_streak} | {self.max_streak}"
