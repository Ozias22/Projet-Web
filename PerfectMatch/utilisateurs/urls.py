from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('connexion/', views.connexion, name='connexion'),
    path("inscription/", views.inscription_view, name="inscription"),
    #path('login/', views.login_view, name='login'),
    # path('compatibilite/<int:match_id>/', views.test_compatibilite, name='test_compatibilite'),
    path("deconnexion/", views.deconnexion, name="deconnexion"),
    # path("connecter_compte/", views.index, name="connecter_compte"),
    path("valider_abonement/", views.valider_abonement, name="valider_abonement"),
    path('profil/', views.profil_view, name='profil'),
    path('accueil/', views.accueil, name='accueil'),
    path('profilPerfectMatch/', views.profil_perfectmatch_view, name='profilPerfectMatch'),
    path("notifications/", views.notifications_view, name="notifications"),

    path("mes-matchs/", views.mes_matchs, name="mes_matchs"),
    path('profil/<int:id>/', views.profil_user_view, name='profil'),
    path('profilPerfectMatch/supprimer-image-ajax/', views.supprimer_image_ajax, name='supprimer_image_ajax'),
    path('api/obtenir_profil/', views.obtenir_profil, name='obtenir_profil'),
    # path('profilPerfectMatch/', views.profil_perfectmatch_view, name='profilPerfectMatch'),
    # path('ajout-image/', views.ajout_image, name='ajout-image'),
    path('discussions/', views.discussions, name='discussions'),
    #API
    path('api/discussions/', views.get_discussions, name='get_discussions'),
    path('api/messages/<int:user_id>/', views.get_messages, name='get_messages'),
]

