from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from .forms import InscriptionForm, AbonnementForm,ConnectionForm,ProfilForm,userProfileForm,ImagesUserForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from .models import User, UserProfile, ImagesUser, Match, Message
from django.db.models import Q
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
@login_required
def obtenir_profil(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    matchs = Match.objects.filter(user1__user=user_profile)
    utilisateurs_profiles = UserProfile.objects.filter(id__exclude=[match.user2.id for match in matchs if match.is_mutual])
    # Filtres ici

    return JsonResponse({'user':user})
    # Convertir les profils en dictionnaires
    # return JsonResponse({
    #     'profiles': [
    #         {
    #             'bio' : utilisateurs_profiles.bio,
    #             'occupation': utilisateurs_profiles.occupation,
    #             'Interets': [interest.name for interest in utilisateurs_profiles.interests.all()],
    #         }]
    # })

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
@login_required
def get_messages(request, user_id):
    current_profile = request.user.profile

    messages = Message.objects.filter(
        Q(sender=current_profile, receiver__id=user_id) |
        Q(sender__id=user_id, receiver=current_profile)
    ).order_by('timestamp')

    data = []
    for msg in messages:
        data.append({
            "id": msg.id,
            "sender": msg.sender.user.username,
            "receiver": msg.receiver.user.username,
            "content": msg.content,
            "timestamp": msg.timestamp.strftime("%Y-%m-%d %H:%M"),
            "is_self": (msg.sender == current_profile)
        })

    return JsonResponse(data, safe=False)
