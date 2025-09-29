from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    # You can add additional fields here if needed
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    country = models.CharField(max_length=50, blank=False)
    city = models.CharField(max_length=50, blank=False)
    password = models.CharField(max_length=12)
    birthday = models.DateField(null=True, blank=False)

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

        constraints = [
            models.UniqueConstraint(fields=['username'], name='unique_username'),
            models.UniqueConstraint(fields=['email'], name='unique_email')
        ]

    def __str__(self):
        return f"{self.username} ({self.email})"