from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone

class User(models.Model):
    GENRE_CHOICES = [
        ('H', 'Homme'),
        ('F', 'Femme'),
    ]

    ROLE_CHOICES = [
        ('J', 'Joueur'),
        ('P', 'Propriétaire'),
    ]

    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mot_de_passe = models.CharField(max_length=100)
    adresse = models.TextField()
    numero_tel = models.CharField(max_length=20)
    niveau = models.CharField(max_length=50)
    genre = models.CharField(max_length=1, choices=GENRE_CHOICES)
    role = models.CharField(max_length=1, choices=ROLE_CHOICES)
    url_image = models.URLField(blank=True, null=True)
    photo_profil = models.ImageField(upload_to='profils/', blank=True, null=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"

class Compte(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(default='default@example.com')
    mot_de_passe = models.CharField(max_length=100)

    def __str__(self):
        return self.email

class Centre(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    adresse = models.TextField()
    nb_terrain = models.PositiveIntegerField()
    gouvernorat = models.CharField(max_length=100, default='Tunis')
    proprietaire = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='centres'
    )

    def __str__(self):
        return f"{self.nom} - {self.adresse}"

class Terrain(models.Model):
    ETAT_CHOICES = [
        ('NR', 'Non réservé'),
        ('R', 'Réservé'),
        ('M', 'Maintenance'),
    ]

    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=50)
    prix = models.DecimalField(max_digits=6, decimal_places=2)
    temps = models.DurationField()
    etat = models.CharField(max_length=2, choices=ETAT_CHOICES, default='NR')
    centre = models.ForeignKey('Centre', on_delete=models.CASCADE, related_name='terrains')

    def __str__(self):
        return f"{self.nom} ({self.get_etat_display()})"

class Reservation(models.Model):
    ETAT_RESERVATION_CHOICES = [
        ('E', 'En attente'),
        ('C', 'Confirmée'),
    ]

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    terrain = models.ForeignKey('Terrain', on_delete=models.CASCADE)
    date_reservation = models.DateTimeField(auto_now_add=True)
    date_jeu_souhaitee = models.DateField()
    heure_debut_souhaitee = models.TimeField()
    nb_personnes = models.PositiveSmallIntegerField(choices=[(i, f"{i} personne(s)") for i in range(1, 5)])
    etat_reservation = models.CharField(max_length=1, choices=ETAT_RESERVATION_CHOICES, default='E')

    def __str__(self):
        return f"Réservation {self.id} - {self.user} ({self.get_etat_reservation_display()})"

class Paiement(models.Model):
    id = models.AutoField(primary_key=True)
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=6, decimal_places=2)
    mode_paiement = models.CharField(max_length=50)
    date_paiement = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Paiement {self.id} - {self.montant} DT"

class Partie(models.Model):
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE)
    temps_de_jeu = models.DurationField()
    score = models.CharField(max_length=100, blank=True, null=True)  # facultatif

    def __str__(self):
        return f"Partie - {self.reservation.date_reservation}"
