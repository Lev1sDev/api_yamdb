from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        USER = "user"
        MODERATOR = "moderator"
        ADMIN = "admin"

    email = models.EmailField('email address', unique=True)
    bio = models.TextField(max_length=300, blank=True, null=True)
    role = models.CharField(
        verbose_name="Степени доступа",
        max_length=10,
        choices=Role.choices,
        default=Role.USER
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "role", ]

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        if self.role == self.Role.ADMIN:
            return True

    @property
    def is_moderator(self):
        if self.role == self.Role.MODERATOR:
            return True


class Confirmation(models.Model):
    email = models.ForeignKey(
        User,
        verbose_name="Почта",
        on_delete=models.SET_NULL,
        null=True,
        related_name="conf"
    )
    confirmation_code = models.CharField(
        verbose_name="Код доступа",
        max_length=100,
        null=False
    )
