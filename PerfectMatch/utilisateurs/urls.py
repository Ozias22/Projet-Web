from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views # Importe le fichier views depuis le dossier courant

urlpatterns = [
    path('', views.index, name='index'),
    path('connexion/', views.connexion, name='connexion'),
    path("inscription/", views.inscription_view, name="inscription"),
    #path('login/', views.login_view, name='login'),
    path('compatibilite/<int:match_id>/', views.test_compatibilite, name='test_compatibilite'),
    path("deconnexion/", views.deconnexion, name="deconnexion"),
    # path("connecter_compte/", views.index, name="connecter_compte"),
    path("valider_abonement/", views.valider_abonement, name="valider_abonement"),
    path('profil/', views.profil_view, name='profil'),
    path('accueil/', views.accueil, name='accueil'),
    path('profilPerfectMatch/', views.profil_perfectmatch_view, name='profilPerfectMatch'),
]
