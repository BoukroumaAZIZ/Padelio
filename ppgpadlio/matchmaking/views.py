from django.shortcuts import redirect, render
from reservation_app.models import User  # si ton User est défini dans users/models.py
from .models import Match

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

from django.views.decorators.http import require_POST

from django.core.mail import send_mail
from django.conf import settings

def matchmaking_home(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('connecter')

    utilisateur = User.objects.get(id=user_id)

    # Récupérer filtres depuis GET (ou aucun si pas présent)
    genre_filtre = request.GET.get('genre')
    niveau_filtre = request.GET.get('niveau')
    lieu_filtre = request.GET.get('lieu')

    candidats = User.objects.exclude(id=utilisateur.id)

    if genre_filtre:
        candidats = candidats.filter(genre=genre_filtre)

    if niveau_filtre:
        candidats = candidats.filter(niveau__icontains=niveau_filtre)

    if lieu_filtre:
        candidats = candidats.filter(adresse__icontains=lieu_filtre)  # filtre sur adresse car lieu_prefere n'existe pas

    # Sinon, tu peux filtrer par défaut par niveau et/ou genre de l'utilisateur (optionnel)

    return render(request, 'matchmaking/matchmaking_home.html', {
        'utilisateur': utilisateur,
        'candidats': candidats,
        'filtres': {
            'genre': genre_filtre or '',
            'niveau': niveau_filtre or '',
            'lieu': lieu_filtre or '',
        }
    })


@require_POST
def choisir(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('connecter')

    utilisateur = User.objects.get(id=user_id)
    cible_id = request.POST.get('cible_id')
    action = request.POST.get('action')  # "like" ou "pass"

    cible = User.objects.get(id=cible_id)

    Match.objects.create(
        utilisateur=utilisateur,
        cible=cible,
        liked=(action == 'like')
    )

    # Vérifie si l'autre a aussi liké
    if action == 'like':
        if Match.objects.filter(utilisateur=cible, cible=utilisateur, liked=True).exists():
            print("🎉 C’est un match !")

    return redirect('matchmaking_home')


@csrf_exempt
def decision_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('user_id')
        decision = data.get('decision')  # 'like' ou 'refuse'

        # TODO : Logique pour enregistrer la décision en base de données (match, refus, etc.)
        print(f"Utilisateur {user_id} a été {decision}")

        return JsonResponse({'status': 'ok', 'message': f'Décision {decision} enregistrée pour user {user_id}'})

    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'}, status=405)



@csrf_exempt
def recevoir_choix(request, cible_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

    user_id = request.session.get('user_id')
    if not user_id:
        print("Erreur : utilisateur non connecté")
        return JsonResponse({'error': 'Utilisateur non connecté'}, status=401)

    try:
        utilisateur = User.objects.get(id=user_id)
        cible = User.objects.get(id=cible_id)
    except User.DoesNotExist:
        print(f"Erreur : utilisateur ou cible non trouvé (user_id={user_id}, cible_id={cible_id})")
        return JsonResponse({'error': 'Utilisateur ou cible introuvable'}, status=404)

    data = json.loads(request.body)
    choix = data.get('choix')
    print(f"Utilisateur {utilisateur.id} a fait un choix: {choix} pour cible {cible.id}")

    if choix == 'like':
        match_obj, created = Match.objects.update_or_create(
            utilisateur=utilisateur,
            cible=cible,
            defaults={'liked': True}
        )
        print(f"Match créé ou mis à jour (liked=True) entre {utilisateur.id} -> {cible.id}")

        # Vérifie le match inverse
        try:
            reverse_match = Match.objects.get(utilisateur=cible, cible=utilisateur)
            print(f"Match inverse trouvé (liked={reverse_match.liked}) entre {cible.id} -> {utilisateur.id}")
            if reverse_match.liked:
                print("Match mutuel détecté !")

                 # Envoi email HTML aux deux joueurs
                subject = "🎾 C’est un match !"

                html_message_utilisateur = f"""
                <html>
                <body style="font-family:Arial, sans-serif; text-align:center;background-color:#ffbd59;">
                    <h2 style="color:#001b79;">🎉 C'est un match !</h2>
                    <p>Salut <strong>{utilisateur.prenom}</strong>,</p>
                    <p>Tu as matché avec <strong>{cible.prenom}</strong> !</p>
                    <img src="https://i.ibb.co/8g8MxPp2/match.png" width="200"/>
                    <p><strong>Email :</strong> {cible.email}<br>
                    <strong>Téléphone :</strong> {cible.numero_tel}</p>
                    <p>Bon match ! 🎾</p>
                    <p>Copyright © Padelio 2025 </p>
                </body>
                </html>
                """

                html_message_cible = f"""
                <html>
                <body style="font-family:Arial, sans-serif; text-align:center;background-color:#ffbd59;>
                    <h2 style="color:#001b79;">🎉 C'est un match !</h2>
                    <p>Salut <strong>{cible.prenom}</strong>,</p>
                    <p>Tu as matché avec <strong>{utilisateur.prenom}</strong> !</p>
                    <img src="https://i.ibb.co/8g8MxPp2/match.png" width="200"/>
                    <p><strong>Email :</strong> {utilisateur.email}<br>
                    <strong>Téléphone :</strong> {utilisateur.numero_tel}</p>
                    <p>Bon match ! 🎾</p>
                    <br><br>
                    <p>Copyright © Padelio 2025 </p>
                </body>
                </html>
                """

                send_mail(subject, '', settings.DEFAULT_FROM_EMAIL, [utilisateur.email], html_message=html_message_utilisateur)
                send_mail(subject, '', settings.DEFAULT_FROM_EMAIL, [cible.email], html_message=html_message_cible)



                return JsonResponse({
                    'status': 'match',
                    'message': 'C’est un match !',
                    'contact': {
                        'email': cible.email,
                        'tel': cible.numero_tel
                    }
                })
        except Match.DoesNotExist:
            print("Pas de match inverse")

        return JsonResponse({'status': 'like enregistré'})

    elif choix == 'refuse':
        Match.objects.update_or_create(
            utilisateur=utilisateur,
            cible=cible,
            defaults={'liked': False}
        )
        print(f"Refus enregistré entre {utilisateur.id} -> {cible.id}")
        return JsonResponse({'status': 'refus enregistré'})

    else:
        print(f"Choix invalide reçu: {choix}")
        return JsonResponse({'error': 'Choix invalide'}, status=400)