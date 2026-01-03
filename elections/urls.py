from django.urls import path
from . import views

app_name = 'elections'

urlpatterns = [
    path('', views.resultats_globaux, name='resultats_globaux'),
    path('centres/', views.resultats_par_centre, name='resultats_par_centre'),
    path('bureaux/', views.resultats_par_bureau, name='resultats_par_bureau'),
    path('bureau/<int:bureau_id>/', views.detail_bureau, name='detail_bureau'),
    path('saisie/', views.saisie_donnees, name='saisie_donnees'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Gestion Candidats
    path('candidats/liste/', views.liste_candidats, name='liste_candidats'),
    path('candidats/ajouter/', views.ajouter_candidat, name='ajouter_candidat'),
    path('candidats/modifier/<int:pk>/', views.modifier_candidat, name='modifier_candidat'),
    path('candidats/supprimer/<int:pk>/', views.supprimer_candidat, name='supprimer_candidat'),
    
    # Gestion Centres
    path('centres/liste/', views.liste_centres, name='liste_centres'),
    path('centres/ajouter/', views.ajouter_centre, name='ajouter_centre'),
    path('centres/modifier/<int:pk>/', views.modifier_centre, name='modifier_centre'),
    path('centres/supprimer/<int:pk>/', views.supprimer_centre, name='supprimer_centre'),
    
    # Gestion Bureaux
    path('bureaux/liste/', views.liste_bureaux, name='liste_bureaux'),
    path('bureaux/ajouter/', views.ajouter_bureau, name='ajouter_bureau'),
    path('bureaux/modifier/<int:pk>/', views.modifier_bureau, name='modifier_bureau'),
    path('bureaux/supprimer/<int:pk>/', views.supprimer_bureau, name='supprimer_bureau'),
]