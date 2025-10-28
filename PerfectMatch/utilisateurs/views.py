from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import InscriptionForm, AbonnementForm,ConnectionForm,ProfilForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login


# Create your views here.

def index(request):
    if request.user is not None:
        redirect('accueil')
    form = ConnectionForm()
    return render(request, "utilisateurs/index.html", {"form": form})

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

def accueil(request):
    return render(request, "utilisateurs/accueil.html")

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
 
    return render(request, "utilisateurs/modifier_profil.html", {"form": form, "user": user})

def modifier_profil(request):
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