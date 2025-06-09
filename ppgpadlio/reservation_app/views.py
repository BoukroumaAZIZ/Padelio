from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from .forms import  FiltreTerrainForm, RechercheReservationForm
from .models import Reservation, User, Terrain
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages 




from .models import Terrain, User

from django.contrib import messages
from django.shortcuts import render, redirect

def home(request):
    user_id = request.session.get('user_id')
    terrains = Terrain.objects.all()[:3]

    # ➤ Traitement du formulaire de contact
    if request.method == 'POST':
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if nom and email and message:
            # Ici tu peux éventuellement enregistrer dans la base ou envoyer par mail
            messages.success(request, 'Message envoyé avec succès !')
        else:
            messages.error(request, 'Veuillez remplir tous les champs.')

        return redirect('home')  # Rediriger vers la même page pour éviter le resoumission du formulaire

    if not user_id:
        return render(request, 'home.html', {'terrains': terrains})

    try:
        utilisateur = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return render(request, 'home.html', {'terrains': terrains})

    return render(request, 'accueil.html', {
        'utilisateur': utilisateur,
        'terrains': terrains
    })



def deconnexion_view(request):
    try:
        del request.session['user_id']
    except KeyError:
        pass
    return redirect('home') 



@csrf_exempt
def reserver(request):
    if request.method == "POST":
        data = json.loads(request.body)
        pays = data.get("pays")
        date = data.get("date")
        nombre = data.get("nombre")
        paiement = data.get("paiement")
        send_mail(
            subject="Confirmation de réservation",
            message=f"Votre réservation pour {nombre} personnes le {date} à {pays} est confirmée. Paiement : {paiement}",
            from_email="ton.email@exemple.com", 
            recipient_list=["utilisateur@example.com"], 
        )

        return JsonResponse({"message": "Réservation réussie et email envoyé."})
    else:
        return JsonResponse({"error": "Méthode non autorisée."}, status=405)




# Vue de réservation via formulaire (HTML)
from django.shortcuts import render, get_object_or_404
from .forms import RechercheReservationForm
from .models import Terrain
# Vue de réservation via formulaire (HTML)
def reserver_formulaire(request):
    from .models import Terrain  # Assurez-vous que c'est importé en haut

def reserver_formulaire(request):
    terrains = []
    if request.method == 'POST':
        form = RechercheReservationForm(request.POST)
        if form.is_valid():
            gouvernorat = form.cleaned_data['gouvernorat']
            date = form.cleaned_data['date_jeu_souhaitee']
            nb_personnes = form.cleaned_data['nb_personnes']
            heure = form.cleaned_data['heure_debut_souhaitee']

            terrains = Terrain.objects.filter(centre__gouvernorat=gouvernorat, etat='NR')

            return render(request, 'reservation.html', {
                'form': form,
                'terrains': terrains,
                'show_results': True,
                'date': date,
                'heure': heure,
                'nb_personnes': nb_personnes
            })
    else:
        form = RechercheReservationForm()

    return render(request, 'reservation.html', {
        'form': form,
        'show_results': False
    })




# API JSON pour réserver depuis le frontend JS
@csrf_exempt
def reserver_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        pays = data.get("pays")
        date = data.get("date")
        nombre = data.get("nombre")
        paiement = data.get("paiement")

        # Envoyer un e-mail de confirmation
        send_mail(
            subject="Confirmation de réservation",
            message=f"Votre réservation pour {nombre} personnes le {date} à {pays} est confirmée. Paiement : {paiement}",
            from_email="ton.email@exemple.com",
            recipient_list=["utilisateur@example.com"],
        )

        return JsonResponse({"message": "Réservation réussie et email envoyé."})
    else:
        return JsonResponse({"error": "Méthode non autorisée."}, status=405)



def rechercher_terrain(request):
    terrains = []
    form = RechercheReservationForm(request.GET or None)

    if form.is_valid():
        gouvernorat = form.cleaned_data.get('gouvernorat')
        nb_personnes = int(form.cleaned_data.get('nb_personnes'))
        terrains = Terrain.objects.filter(centre__gouvernorat=gouvernorat, etat='NR')

    return render(request, 'recherche_terrains.html', {'form': form, 'terrains': terrains})



def connexion_view(request):
    return render(request, 'connecter.html')
#connecter 

def connexion_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        mot_de_passe = request.POST.get('mot_de_passe')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, 'connecter.html', {'erreur': 'Email ou mot de passe incorrect.'})

        if user.mot_de_passe == mot_de_passe:
            # Connexion réussie — ici, tu peux par exemple stocker l'ID utilisateur en session
            request.session['user_id'] = user.id
            return redirect(home)  # rediriger vers une page après connexion
        else:
            return render(request, 'connecter.html', {'erreur': 'Email ou mot de passe incorrect.'})

    return render(request, 'connecter.html')



#def creer_compte_view(request):
 #   return render(request, 'creerCompte.html')

#creation de compte 
def creer_compte_view(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        email = request.POST.get('email')
        mot_de_passe = request.POST.get('mot_de_passe')
        confirmer_mdp = request.POST.get('confirmer_mdp')
        adresse = request.POST.get('adresse')
        numero_tel = request.POST.get('numero_tel')
        niveau = request.POST.get('niveau')
        genre = request.POST.get('genre')
        role = request.POST.get('role')

        if mot_de_passe != confirmer_mdp:
            return render(request, 'creerCompte.html', {
                'erreur': 'Les mots de passe ne correspondent pas.'
            })

        # Vérifie si l'utilisateur existe déjà
        if User.objects.filter(email=email).exists():
            return render(request, 'creerCompte.html', {
                'erreur': 'Cet email est déjà utilisé.'
            })

        # Crée le nouvel utilisateur
        User.objects.create(
            nom=nom,
            prenom=prenom,
            email=email,
            mot_de_passe=mot_de_passe,  # à sécuriser avec hash pour une vraie app
            adresse=adresse,
            numero_tel=numero_tel,
            niveau=niveau,
            genre=genre,
            role=role
        )

        messages.success(request, 'Compte créé avec succès. Vous pouvez vous connecter.')
        return redirect('connecter')    
    return render(request, 'creerCompte.html')




from django.core.mail import send_mail
from django.utils.html import format_html

@require_POST
def confirmer_reservation(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('connecter')

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect('connecter')

    terrain_id = request.POST.get('terrain_id')
    date = request.POST.get('date_jeu_souhaitee')
    heure = request.POST.get('heure_debut_souhaitee')
    nb_personnes = request.POST.get('nb_personnes')

    try:
        terrain = Terrain.objects.get(id=terrain_id)
    except Terrain.DoesNotExist:
        return redirect('reserver_formulaire')

    reservation = Reservation.objects.create(
        user=user,
        terrain=terrain,
        date_jeu_souhaitee=date,
        heure_debut_souhaitee=heure,
        nb_personnes=nb_personnes,
        etat_reservation='E'
    )

    # ✅ Contenu HTML du mail
    html_message = f"""
        <html>
        <body>
            <h2>Confirmation de réservation 🎾</h2>
            <p>Bonjour <strong>{user.prenom} {user.nom}</strong>,</p>
            <p>Merci pour votre réservation sur notre plateforme de padel ! Voici les détails :</p>
            <ul>
                <li><strong>Terrain :</strong> {terrain.nom}</li>
                <li><strong>Adresse :</strong> {terrain.centre.adresse}</li>
                <li><strong>Date :</strong> {date}</li>
                <li><strong>Heure :</strong> {heure}</li>
                <li><strong>Nombre de personnes :</strong> {nb_personnes}</li>
            </ul>
            <p>Nous vous attendons avec impatience pour une belle partie !</p>
            <br>
            <p style="color: gray; font-size: 12px;">Ce mail est automatique, merci de ne pas y répondre.</p>
        </body>
        </html>
    """

    try:
        send_mail(
            subject="🎾 Confirmation de votre réservation de padel",
            message="Votre réservation est confirmée.",  # version texte brut (fallback)
            from_email="noreply@padelapp.com",
            recipient_list=[user.email],
            fail_silently=False,
            html_message=html_message
        )
    except Exception as e:
        print(f"Erreur lors de l'envoi du mail : {e}")

    return render(request, 'confirmation.html', {'reservation': reservation})


from django.contrib.auth.decorators import login_required

def mes_reservations(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('connecter')  # Rediriger vers la page de connexion si pas connecté

    try:
        utilisateur  = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect('connecter')

    reservations = Reservation.objects.filter(user=utilisateur ).order_by('-date_reservation')

    return render(request, 'mes_reservations.html', {'utilisateur': utilisateur,'reservations': reservations})


def tous_terrains(request):
    form = FiltreTerrainForm(request.GET or None)
    terrains = Terrain.objects.all()

    if form.is_valid():
        gouvernorat = form.cleaned_data.get('gouvernorat')
        type_terrain = form.cleaned_data.get('type')
        prix_max = form.cleaned_data.get('prix_max')

        if gouvernorat:
            terrains = terrains.filter(gouvernorat=gouvernorat)
        if type_terrain:
            terrains = terrains.filter(type=type_terrain)
        if prix_max is not None:
            terrains = terrains.filter(prix__lte=prix_max)

    return render(request, 'tous_terrains.html', {
        'form': form,
        'terrains': terrains
    })


def contact(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        sujet = request.POST.get('sujet')
        message = request.POST.get('message')

        full_message = f"Message de {nom} ({email})\n\n{sujet}\n\n{message}"

        send_mail(
            subject=f"Nouveau message de {nom} - {sujet}",
            message=full_message,
            from_email='votre_email@example.com',
            recipient_list=['boukrouma.ma@gmail.com'],  # Change à ton adresse admin
            fail_silently=False,
        )

        messages.success(request, "Votre message a été envoyé avec succès.")
        return redirect('contact')

    return render(request, 'contact.html')


from django.shortcuts import render, redirect
from .models import User

def profile(request):
    user_id = request.session.get('user_id')

    if not user_id:
        # Si pas connecté, rediriger vers login ou home
        return redirect('login')  # adapte selon ton url

    try:
        utilisateur = User.objects.get(id=user_id)
    except User.DoesNotExist:
        # Si utilisateur non trouvé, rediriger ou afficher message
        return redirect('login')

    return render(request, 'profile.html', {'utilisateur': utilisateur})


def profile_update(request):
    user_id = request.session.get('user_id')
    utilisateur = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        utilisateur.nom = request.POST.get('nom')
        utilisateur.prenom = request.POST.get('prenom')
        utilisateur.adresse = request.POST.get('adresse')
        utilisateur.numero_tel = request.POST.get('numero_tel')
        utilisateur.niveau = request.POST.get('niveau')
        utilisateur.genre = request.POST.get('genre')
        utilisateur.role = request.POST.get('role')

        if request.FILES.get('photo_profil'):
            utilisateur.photo_profil = request.FILES['photo_profil']

        utilisateur.save()
        return redirect('profile')  # Redirection vers la page profil

    return render(request, 'profile_update.html', {'utilisateur': utilisateur})

