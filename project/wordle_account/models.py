from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email
from django.utils import timezone
from django.db.models import Q
from .utils import load_preface_list
from random import randint


# Create your models here.


class CustomUser(AbstractUser):

    email = models.EmailField(
        verbose_name="email address",
        unique=True,
        validators=[validate_email],
        error_messages={
            "unique": "A user with that email already exists.",
        },
    )

    REQUIRED_FIELDS = ["username"]

    USERNAME_FIELD = "email"

    _members = load_preface_list()

    def __str__(self) -> str:
        return self.email

    @classmethod
    def random_preface_user(cls):
        """
        SELECT ...
        FROM wordle_account_customuser
        LEFT OUTER JOIN wordle_app_game ON
        wordle_account_customuser.id = wordle_app_game.player_id
        WHERE wordle_account_customuser.email LIKE 'preface'
        AND wordle_app_game.created_at IS NULL OR wordle_app_game.created_at < ...
        """
        users = CustomUser.objects.all().filter(
            Q(email__icontains="preface"),
            Q(games__created_at__isnull=True)
            | Q(games__created_at__lt=timezone.localtime()),
        )

        return users[randint(0, len(users) - 1)]

    @staticmethod
    def create_preface_users():
        members = CustomUser._members
        entries = map(
            lambda name: CustomUser(
                username=name,
                email=f"{name}@preface.com",
                password="prefaceCoding",
            ),
            members,
        )
        CustomUser.objects.bulk_create(entries)

        print("seeded preface users")
