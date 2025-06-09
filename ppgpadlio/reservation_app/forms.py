from django import forms
from .models import Reservation

GOUVERNORATS_CHOICES = [
    ('Tunis', 'Tunis'), ('Ariana', 'Ariana'), ('Ben Arous', 'Ben Arous'),
    ('Manouba', 'Manouba'), ('Sfax', 'Sfax'), ('Sousse', 'Sousse'),
    ('Gabès', 'Gabès'), ('Nabeul', 'Nabeul'), ('Monastir', 'Monastir'),
    ('Bizerte', 'Bizerte')
]

NB_PERSONNES_CHOICES = [(i, f"{i} personne(s)") for i in range(1, 5)]

MODE_PAIEMENT_CHOICES = [
    ('tous', 'Tout le terrain'),
    ('1part', 'Une part'),
    ('2part', 'Deux parts'),
    ('3part', 'Trois parts'),
    ('sur_place', 'Sur place'),
]


class RechercheReservationForm(forms.Form):
    gouvernorat = forms.ChoiceField(
        choices=GOUVERNORATS_CHOICES,
        label="Gouvernorat",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    date_jeu_souhaitee = forms.DateField(
        label="Date souhaitée",
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )

    heure_debut_souhaitee = forms.TimeField(
        label="Heure souhaitée",
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'form-control'
        })
    )

    nb_personnes = forms.ChoiceField(
        choices=NB_PERSONNES_CHOICES,
        label="Nombre de personnes",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    mode_paiement = forms.ChoiceField(
        choices=MODE_PAIEMENT_CHOICES,
        label="Mode de paiement",
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class FiltreTerrainForm(forms.Form):
    gouvernorat = forms.CharField(required=False, label="Gouvernorat")
    type = forms.CharField(required=False, label="Type de terrain")
    prix_max = forms.IntegerField(required=False, label="Prix max")
    

class RechercheTerrainForm(forms.Form):
    gouvernorat = forms.ChoiceField(choices=GOUVERNORATS_CHOICES, label="Gouvernorat")
    date_jeu_souhaitee = forms.DateField(label="Date souhaitée", widget=forms.DateInput(attrs={'type': 'date'}))
    heure_debut_souhaitee = forms.TimeField(label="Heure de début", widget=forms.TimeInput(attrs={'type': 'time'}))
    nb_personnes = forms.IntegerField(label="Nombre de personnes")
 
