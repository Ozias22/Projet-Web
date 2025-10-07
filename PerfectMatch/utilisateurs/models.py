from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError

# Create your models here.
class User(AbstractUser):
    
    username = models.CharField(max_length=50, unique=True,  validators=[MinLengthValidator(3, "Le nom d'utilisateur doit contenir au moins 3 caractères.")])
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=False,  validators=[MinLengthValidator(3, "Le nom d'utilisateur doit contenir au moins 3 caractères.")])
    last_name = models.CharField(max_length=30, blank=False,  validators=[MinLengthValidator(3, "Le nom d'utilisateur doit contenir au moins 3 caractères.")])
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