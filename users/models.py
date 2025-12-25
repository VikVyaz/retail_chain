from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя"""

    username = models.CharField(
        unique=True,
        verbose_name='Username',
        help_text='Username пользователя'
    )
    email = models.EmailField(
        unique=True,
        blank=True,
        null=True,
        verbose_name="Email",
        help_text='Email пользователя'
    )

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.username} - {self.email}"

    class Meta:
        verbose_name = "Пользователи"
        verbose_name_plural = "Пользователь"
