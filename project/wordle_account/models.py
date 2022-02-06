from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email


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

    def __str__(self) -> str:
        return self.email
