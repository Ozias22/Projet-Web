from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from .forms import InscriptionForm, AbonnementForm,ConnectionForm,ProfilForm,userProfileForm,ImagesUserForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from .models import User, UserProfile, ImagesUser,Match
from django.core import serializers
import json
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

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
                return redirect('accueil')
            else:
                form.add_error(None, "Nom d'utilisateur ou mot de passe incorrect.")
    else:
        form = ConnectionForm()
    return render(request, "utilisateurs/connecter_compte.html",{'form': form})


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
    """Vue pour modifier le profil de l'utilisateur connecté"""
    user = request.user

    if request.method == "POST":
        form = ProfilForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre profil a été mis à jour avec succès")
            return redirect("profil")
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        form = ProfilForm(instance=user)

    return render(request, "utilisateurs/modifier_profil.html", {"form": form})

@login_required
def profil_perfectmatch_view(request):
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

def obtenir_profil(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    matchs = Match.objects.filter(user1_id__user=user.id)

    if matchs is not None:
        profiles_non_valides = [i for i in matchs if i.is_mutual]
        utilisateurs_profiles = UserProfile.objects.exclude(id__in=[profiles_non_valide.user2_id for profiles_non_valide in profiles_non_valides])
        imagesUsers = ImagesUser.objects.filter(user__in=[utilisateur_profile.user for utilisateur_profile in utilisateurs_profiles])
    else:
        utilisateurs_profiles = UserProfile.objects.all()
        imagesUsers = ImagesUser.objects.filter(user__in=[utilisateur_profile.user for utilisateur_profile in utilisateurs_profiles])
    # return JsonResponse({'profiles': serializers.serialize('json', utilisateurs_profiles),'Images':serializers.serialize('json', imagesUsers)}, safe=False)

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
        match = Match.objects.get_or_create(user1=profil_actuel, user2=profil_recherche)
        # si l'autre a déjà liké, marquer mutuel
        reverse = Match.objects.filter(user1=profil_recherche, user2=profil_actuel).first()
        if reverse:
            match.is_mutual = True
            reverse.is_mutual = True
            match.save()
            reverse.save()
            return JsonResponse({'result': 'match', 'mutual': True})
        return JsonResponse({'result': 'liked', 'mutual': False})
    elif action == 'dislike':
        return JsonResponse({'result': 'disliked'})
    else:
        return JsonResponse({'error': 'Unknown action'}, status=400)

# @login_required
# def profil_user_view(request, id):
#     """Vue pour afficher le profil d’un utilisateur donné"""
#     user = get_object_or_404(User, id=id)
#     user_profile = UserProfile.objects.get(user=user)
#     imagesUser = ImagesUser.objects.filter(user=user)

#     form1 = userProfileForm(instance=user_profile)
#     form2 = ImagesUserForm()

#     return render(
#         request,
#         "utilisateurs/profilePerfectMatch.html",
#         {"form1": form1, "form2": form2, "ImagesUser": imagesUser}
#     )