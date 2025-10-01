from django.urls import path
from . import views # Importe le fichier views depuis le dossier courant

urlpatterns = [
    path('', views.index, name='index'),
    path('connexion/', views.connexion, name='connexion'),
    path("inscription/", views.inscription_view, name="inscription"),
    path("accueil/", views.accueil, name='accueil'),
    # path("valider_abonement/", views.valider_abonement, name='valider_abonement'),
]