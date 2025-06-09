from django.urls import path
from . import views
from matchmaking.views import recevoir_choix
urlpatterns = [
    path('', views.matchmaking_home, name='matchmaking_home'),
    path('choisir/', views.choisir, name='choisir'),
    path('decision/', views.decision_view, name='decision'),
    path('matchmaking/choix/<int:cible_id>/', recevoir_choix, name='recevoir_choix'),

]