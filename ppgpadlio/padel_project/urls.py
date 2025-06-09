"""
URL configuration for padel_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from padel_project import settings
from . import views
from reservation_app import views
from matchmaking import views as matchmaking_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('reservation_app.urls')),
    path('', views.home, name='home'), 
    path('logout/', views.deconnexion_view, name='logout'),

    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.profile_update, name='profile_update'),


   
    
    path('confirmer-reservation/', views.confirmer_reservation, name='confirmer_reservation'),
    path('reserver/', views.reserver_formulaire, name='reserver_formulaire'),
    path('api/reserver/', views.reserver_api, name='reserver_api'),
    path('recherche-terrains/', views.rechercher_terrain, name='rechercher_terrain'),
    path('reserver/<int:terrain_id>/', views.reserver_formulaire, name='reserver_formulaire'),

    path('mes-reservations/', views.mes_reservations, name='mes_reservations'),
    
    
    path('admin/', admin.site.urls),
    path('connecter/', views.connexion_view, name='connecter'),
    path('creerCompte/', views.creer_compte_view, name='creerCompte'),
    path('matchmaking/', include('matchmaking.urls')),
    path('terrains/', views.tous_terrains, name='tous_terrains'),

    path('matchmaking/choisir/', matchmaking_views.choisir, name='choisir'),
    path('matchmaking/decision/', matchmaking_views.decision_view, name='decision'),
    path('matchmaking/choix/<int:cible_id>/', matchmaking_views.recevoir_choix, name='recevoir_choix'),
    

    path('contact/', views.contact, name='contact')
]

from django.conf.urls.static import static
from django.conf import settings

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)