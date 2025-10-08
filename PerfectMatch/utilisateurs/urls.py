from django.urls import path
from . import views # Importe le fichier views depuis le dossier courant

urlpatterns = [
    path('', views.index, name='index'),
    path('connexion/', views.connexion, name='connexion'),
    path("inscription/", views.inscription_view, name="inscription"),
<<<<<<< HEAD
    path("accueil/", views.accueil, name='accueil'),
    path("profil/", views.profil_view, name='profil'),
    path("profil/modifier/", views.modifier_view, name='profil_modifier'),
    # path("valider_abonement/", views.valider_abonement, name='valider_abonement'),
=======
    # path("connecter_compte/", views.index, name="connecter_compte"),
    path("valider_abonement/", views.valider_abonement, name="valider_abonement"),
>>>>>>> origin/main
]