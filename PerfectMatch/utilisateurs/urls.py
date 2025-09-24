from django.urls import path
from . import views # Importe le fichier views depuis le dossier courant

urlpatterns = [
    path('', views.index, name='index'),
    path('connexion', views.connexion, name='connexion')
]