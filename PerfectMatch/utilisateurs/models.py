from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
import os

from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError


def validate_file_extension(value):
    """Valide l'extension du fichier téléversé"""
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.pdf', '.doc', '.docx']
    ext = os.path.splitext(value.name)[1].lower()
    if ext not in allowed_extensions:
        raise ValidationError(f'Type de fichier non autorisé: {ext}')

def validate_file_size(value):
    """Valide la taille du fichier (5MB max)"""
    filesize = value.size
    if filesize > 5 * 1024 * 1024:  # 5MB
        raise ValidationError('Le fichier est trop volumineux (5MB maximum)')
# Create your models here.
class User(AbstractUser):
    
    username = models.CharField(max_length=50, unique=True,  validators=[MinLengthValidator(3, "Le nom d'utilisateur doit contenir au moins 3 caractères.")])
    email = models.EmailField(unique=True)
    photo_profil = models.ImageField(verbose_name='image_de_profil',upload_to='images/%Y/%m/%d/',validators=[validate_file_extension,validate_file_size],blank=True)
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    country = models.CharField(max_length=50, blank=False)
    city = models.CharField(max_length=50, blank=False)
    password = models.CharField(max_length=12)
    birthday = models.DateField(null=True, blank=False)
    photo_profil = models.ImageField(
        upload_to="profils/",
        blank=True,
        null=True,
        default="profils/default.png"
    )

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

        constraints = [
            models.UniqueConstraint(fields=['username'], name='unique_username'),
            models.UniqueConstraint(fields=['email'], name='unique_email')
        ]

    def __str__(self):
        return f"{self.username} ({self.email})"


class Abonement(models.Model):
    TYPE_CHOICES = [
        ('mensuel', 'Mensuel'),
        ('annuel', 'Annuel'),
        ('premium', 'Premium'),
    ]
    type_abonement = models.CharField(max_length=20, choices=TYPE_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='abonements')
    start_date = models.DateField(auto_now_add=True)
    card_number = models.CharField(max_length=16)
    expiration_date = models.DateField()
    cvv = models.CharField(max_length=4)


    def __str__(self):
        return f"{self.type_abonement} starting {self.start_date}"
    class Meta:
        verbose_name = 'abonement'
        verbose_name_plural = 'abonements'
        constraints = [
            models.UniqueConstraint(fields=['user', 'type_abonement'], name='unique_user_abonement')
        ]
