from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import InscriptionForm, AbonnementForm,ConnectionForm,ProfilForm,userProfileForm,ImagesUserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from .models import User, UserProfile, ImagesUser

# Create your views here.

# def index(request):
#     form = ConnectionForm()
#     return render(request, "utilisateurs/connecter_compte.html", {"form": form})
def index(request):
    # return render(request, "utilisateurs/accueil.html")
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
    """Vue pour afficher le profil PerfectMatch de l'utilisateur connecté"""

    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    imagesUser = ImagesUser.objects.filter(user=user)

    form1 = userProfileForm(instance=user_profile)
    form2 = ImagesUserForm()

    return render(request, "utilisateurs/profilePerfectMatch.html", {"form1": form1, "form2": form2, "ImagesUser": imagesUser})

def ajouter_image_view(request):
    """Vue pour ajouter une image au profil PerfectMatch de l'utilisateur connecté"""
    if request.method == "POST":
        form = ImagesUserForm(request.POST, request.FILES)
        if form.is_valid():
            image_user = form.save(commit=False)
            image_user.user = request.user
            image_user.save()
            messages.success(request, "Image ajoutée avec succès !")
        else:
            messages.error(request, "Erreur lors de l'ajout de l'image. Veuillez réessayer.")
    return redirect("profile_perfectmatch")