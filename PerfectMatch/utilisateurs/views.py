import json
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from .forms import InscriptionForm, AbonnementForm,ConnectionForm,ProfilForm,userProfileForm,ImagesUserForm,TestCompatibiliteForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from .models import User, UserProfile, ImagesUser, Compatibilite, Message, Match
from django.core import serializers
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import date
from django.db.models.functions import Random
from datetime import date
from django.db.models.functions import Random

def index(request):
    return redirect("connexion")

def inscription_view(request):
    if request.method == "POST":
        form = InscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Votre compte a été créé avec succès !")
            return redirect("connexion")
        else:
            messages.add_message(request, messages.ERROR, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = InscriptionForm()

    return render(request, "utilisateurs/inscription.html", {"form": form})

def valider_abonement(request):
    if request.method == "POST":
        form = AbonnementForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Votre abonnement a été validé avec succès !")
            return redirect("connecter_compte")
        else:
            messages.add_message(request, messages.ERROR, "Veuillez corriger les erreurs ci-dessous.")

    else:
        form = AbonnementForm()

    return render(request, "utilisateurs/abonement.html", {"form": form})

def deconnexion(request):
    """Comment"""
    logout(request)
    messages.success(request, "Vous avez été déconnecté avec succès.")
    return redirect('connexion')


def connexion(request):
    """Comment"""
    if request.user.is_authenticated:
        return redirect('accueil')

    if request.method == "POST":
        form = ConnectionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Connexion réussie !")

                from utilisateurs.models import UserProfile

                profile, created = UserProfile.objects.get_or_create(user=user)

                if profile.first_login:
                    profile.first_login = False
                    profile.save()
                    return redirect('profilPerfectMatch')
                return redirect('accueil')
            else:
                form.add_error(None, "Nom d'utilisateur ou mot de passe incorrect.")
    else:
        form = ConnectionForm()

    return render(request, "utilisateurs/connecter_compte.html", {'form': form})


@login_required
def accueil(request):
    """Vue pour la page d'accueil après connexion"""
    user = request.user
    return render(request, "utilisateurs/accueil.html", {"user": user})

@login_required
def profil_view(request):
    """Vue pour afficher le profil de l'utilisateur connecté"""
    user = request.user
    return render(request, "utilisateurs/profil.html", {"user": user})


@login_required
def modifier_view(request):
    user = request.user
    if request.method == "POST":
        form = ProfilForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Votre profil a été mis à jour avec succès !")
            return redirect('modif_profil')
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        form = ProfilForm(instance=user)
    return render(request, "utilisateurs/modif_profil.html", {"form": form})

@login_required
def test_compatibilite(request, match_id):
    if request.user.id == match_id:
        messages.error(request, "Vous ne pouvez pas faire un test de compatibilité avec vous-même.")
        return redirect("mes_matchs")

    match = Match.objects.get(id=match_id)

    if request.method == "POST":
        form = TestCompatibiliteForm(request.POST)
        if form.is_valid():
            user_answers = form.cleaned_data
            score = 0
            total = len(user_answers)

            for value in user_answers.values():
                if value == "oui":
                    score += 1

            score_final = (score / total) * 100

            user1  = User.objects.get(id=match.user1_id)
            user2  = User.objects.get(id=match.user2_id)
            Compatibilite.objects.update_or_create(
                utilisateur=user1,
                match=user2,
                defaults={'score': score_final}
            )

            return render(request, "utilisateurs/compatibilite_resultat.html", {
                "match": match,
                "score": score_final
            })
    else:
        form = TestCompatibiliteForm()

    return render(request, "utilisateurs/compatibilite_form.html", {
        "form": form,
        "match": match
    })


def profil_perfectmatch_view(request):
    """Vue pour afficher le profil PerfectMatch de l'utilisateur connecté"""
    user = request.user
    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        user_profile = None

    imagesUser = ImagesUser.objects.filter(user=user)

    if request.method == "POST":
        form1 = userProfileForm(request.POST, instance=user_profile)
        form2 = ImagesUserForm(request.POST, request.FILES)

        # Si formulaire profil soumis
        if 'occupation' in request.POST or 'bio' in request.POST:
            if form1.is_valid():
                form1.save(user=user)
                user_profile = UserProfile.objects.get(user=user)

        # Si formulaire image soumis
        if 'image' in request.FILES:
            if form2.is_valid():
                form2.save(user=user)
                imagesUser = ImagesUser.objects.filter(user=user)

    else:
        form1 = userProfileForm(instance=user_profile)
        form2 = ImagesUserForm()

    return render(
        request,
        "utilisateurs/profilePerfectMatch.html",
        {
            "form1": form1,
            "form2": form2,
            "ImagesUser": imagesUser
        }
    )

@login_required
def obtenir_profil(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)

    # PARAMETRES FILTRES
    gender = request.GET.get("gender")
    city = request.GET.get("city")
    country = request.GET.get("country")
    min_age = request.GET.get("min_age")
    max_age = request.GET.get("max_age")

    # Parse en int des ages
    if min_age:
        min_age = int(min_age)
    if max_age:
        max_age = int(max_age)


    matchs = Match.objects.filter(user1_id__user=user.id)
    if matchs is not None:
        profiles_non_valides = []
        for i in matchs:
            if i.is_mutual:
                profiles_non_valides.append(i)
        utilisateurs_profiles = UserProfile.objects.exclude(id__in=[profiles_non_valide.user2_id for profiles_non_valide in profiles_non_valides]).exclude(user=user)
        # imagesUsers = ImagesUser.objects.filter(user__in=[utilisateur_profile.user for utilisateur_profile in utilisateurs_profiles])
        users = []
        for profil in utilisateurs_profiles:
            if profil.user_id:  # évite les profils orphelins
                users.append(profil.user)

        imagesUsers = ImagesUser.objects.filter(user__in=users)

    else:
        utilisateurs_profiles = UserProfile.objects.exclude(user=user)
        imagesUsers = ImagesUser.objects.filter(user__in=[utilisateur_profile.user for utilisateur_profile in utilisateurs_profiles])
    # return JsonResponse({'profiles': serializers.serialize('json', utilisateurs_profiles),'Images':serializers.serialize('json', imagesUsers)}, safe=False)

    # AJOUT DES FILTRES POUR GET PROFILES
    # Genre selon UseProfile
    if gender:
        utilisateurs_profiles = utilisateurs_profiles.filter(gender__iexact=gender)
    # Ville selon User
    if city:
        utilisateurs_profiles = utilisateurs_profiles.filter(user__city__icontains=city)
    # Pays selon User
    if country:
        utilisateurs_profiles = utilisateurs_profiles.filter(user__country__icontains=country)
    # Age selon date et aujourdhui
    today = date.today()
    if min_age:
        max_birthdate = today.replace(year=today.year - min_age)
        utilisateurs_profiles = utilisateurs_profiles.filter(user__birthday__lte=max_birthdate)
    if max_age:
        min_birthdate = today.replace(year=today.year - max_age)
        utilisateurs_profiles = utilisateurs_profiles.filter(user__birthday__gte=min_birthdate)
    # Mettre la liste en aleatoire
    utilisateurs_profiles = utilisateurs_profiles.order_by(Random())

    # Construire une liste de profils avec l'objet user inclus (dictionnaire sérialisable)
    profils_serialises = []
    for up in utilisateurs_profiles:
        user = up.user
        profils_serialises.append({
            'id': up.id,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'birthday': user.birthday.strftime('%Y-%m-%d') if user.birthday else None,
                'country': user.country,
                'city': user.city,
                'photo_profil': f"/media/{user.photo_profil.name}",
            },
            'gender': up.gender,
            'occupation': up.occupation,
            'bio': up.bio,
            'interests': [i.name for i in up.interests.all()],
        })

    imagesUsers = list(imagesUsers.values())
    for img in imagesUsers:
        img['image'] = f"/media/{img['image']}"

    return JsonResponse({'profiles': profils_serialises, 'Images': imagesUsers})





@csrf_exempt
def action_like(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

    try:
        donnees = json.loads(request.body)
    except Exception:
        return JsonResponse({'error': 'JSON Invalide'}, status=400)

    target_user_id = donnees.get('user_id')
    action = donnees.get('action')

    if not target_user_id or not action:
        return JsonResponse({'error': 'Champs manquants'}, status=400)


    if not request.user or not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication requise'}, status=401)

    try:
        target_user = User.objects.get(id=target_user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Utilisateur inexistant'}, status=404)

    try:
        profil_actuel = UserProfile.objects.get(user=request.user)
        profil_recherche = UserProfile.objects.get(user=target_user)
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'Profil utilisateur manquant'}, status=404)

    if action == 'like':
        match = Match.objects.create(user1=profil_actuel, user2=profil_recherche)
        print("Match créé ou récupéré:", match)
        # si l'autre a déjà liké, marquer mutuel
        reverse = Match.objects.filter(user1=profil_recherche, user2=profil_actuel).first()
        if reverse:
            match.is_mutual = 1
            reverse.is_mutual = 1
            match.save()
            reverse.save()
            return JsonResponse({'result': 'liked', 'mutual': 1,'utilisateur': target_user.username,'match': match.id})
        return JsonResponse({'result': 'liked', 'mutual': 0})
    elif action == 'dislike':
        return JsonResponse({'result': 'disliked'})
    else:
        return JsonResponse({'error': 'Unknown action'}, status=400)

@login_required
def discussions(request):
    return render(request,"utilisateurs/discussions.html")

@login_required
def get_discussions(request):
    current_profile = request.user.profile

    # Obtient les utilisateurs qui on interagis avec l'utilisateur courant
    pairs = Message.objects.filter(
        Q(sender=current_profile) | Q(receiver=current_profile)
    ).values_list("sender_id", "receiver_id").distinct()

    discussion_profile_ids = set()
    # Filtre les utilisateurs en contact pour l'affichage des discussions
    for sender_id, receiver_id in pairs:
        if sender_id != current_profile.id:
            discussion_profile_ids.add(sender_id)
        if receiver_id != current_profile.id:
            discussion_profile_ids.add(receiver_id)

    # Obtentions des donnes autres utilisateurs
    other_users = User.objects.filter(profile__id__in=discussion_profile_ids)

    data = [
        {
            "id": user.id,
            "username": user.username,
        }
        for user in other_users
    ]

    return JsonResponse(data, safe=False)


@login_required
def get_messages(request, user_id):
    current_profile = request.user.profile
    sender_profile = get_object_or_404(UserProfile, user__id=user_id)

    print(sender_profile)
    messages_list = Message.objects.filter(
        Q(receiver_id=current_profile.id, sender_id=sender_profile.id) |
        Q(receiver_id=sender_profile.id, sender_id=current_profile.id)
    ).order_by('timestamp')

    data = []
    for msg in messages_list:
        data.append({
            "id": msg.id,
            "sender": msg.sender.user.username,
            "receiver": msg.receiver.user.username,
            "content": msg.content,
            "timestamp": msg.timestamp.strftime("%Y-%m-%d %H:%M"),
            "is_self": (msg.sender == current_profile)
        })

    return JsonResponse(data, safe=False)

@login_required
def notifications_view(request):

    profile = request.user.profile

    unread_messages = Message.objects.filter(receiver=profile, is_read=False).order_by('-timestamp')
    match_not_mutual = Match.objects.filter(
        user2_id = profile,
        is_mutual = False
    )
    print('match',match_not_mutual)

    data = [

        {
            "id": msg.id,
            "sender": msg.sender.user.username,
            "content": msg.content,
            "timestamp": msg.timestamp.strftime("%Y-%m-%d %H:%M")
        }
        for msg in unread_messages
    ]
    unread_messages.update(is_read=True)

    return JsonResponse({"messages": data})

@csrf_exempt
@login_required
def envoyer_message(request,receiver_Id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

    try:
        donnees = json.loads(request.body)
    except Exception:
        return JsonResponse({'error': 'JSON Invalide'}, status=400)

    content = donnees.get('content')

    if not receiver_Id or not content:
        return JsonResponse({'error': 'Champs manquants'}, status=400)
    try:
        receiver_profile = UserProfile.objects.get(user__id=receiver_Id)
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'Profil utilisateur manquant'}, status=404)
    sender_profile = request.user.profile
    message = Message.objects.create(
        sender=sender_profile,
        receiver=receiver_profile,
        content=content
    )
    if message:
        message.save()
        return JsonResponse({'result': 'Message envoyé avec succès'})
    else:
        return JsonResponse({'error': 'Échec de l\'envoi du message'}, status=500)

@login_required
def mes_matchs(request):
    profil_actuel = UserProfile.objects.get(user=request.user)
    matchs = Match.objects.filter(user1 = profil_actuel, is_mutual=True)
    return render(request, 'utilisateurs/mes_matchs.html', {'matchs': matchs})

@login_required
def supprimer_image(request,id):
    image_id = id

    if not image_id:
        return JsonResponse({"success": False, "error": "ID manquant"})

    try:
        image = ImagesUser.objects.get(id=image_id, user=request.user)
        image.delete()
    except ImagesUser.DoesNotExist:
        return JsonResponse({"success": False, "error": "Image introuvable"})

    return redirect('profilPerfectMatch')