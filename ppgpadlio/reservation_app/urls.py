from django.urls import path
from . import views


urlpatterns = [
    path('reservation/', views.reserver, name='reservation'),

     path('reserver/', views.reserver_formulaire, name='reserver_formulaire'),
    path('api/reserver/', views.reserver_api, name='reserver_api'),
    path('recherche-terrains/', views.rechercher_terrain, name='rechercher_terrain'),
]



