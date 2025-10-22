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
    photo_profil = models.ImageField(upload_to='photos_profils/', blank=True, null=True) 
 
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
 
        constraints = [
            models.UniqueConstraint(fields=['username'], name='unique_username'),
            models.UniqueConstraint(fields=['email'], name='unique_email')
        ]
 
    def __str__(self):
        return f"{self.username} ({self.email})"
    

class Compatibilite(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tests_effectues')
    match = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tests_recus')
    score = models.FloatField(default=0)
    date_test = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Compatibilité entre {self.utilisateur.username} et {self.match.username} : {self.score:.1f}%"