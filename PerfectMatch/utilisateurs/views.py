from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import InscriptionForm, ConnectionForm, ProfilForm
from .models import User
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    """Comment"""
    return render(request, "utilisateurs/index.html")

def connexion(request):
    """Comment"""
    if request.method == "POST":
        form = ConnectionForm(request.POST)
        if form.is_valid():
            try:
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]
                
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = None
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                
                login(request, user)
                messages.success(request,"Connexion a été fait avec succès.")
                return redirect('accueil')
            else:
                form.add_error(None, "Invalid email or password.")
                
                
            return redirect('index')
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

def inscription_view(request):
    if request.method == "POST":
        form = InscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre compte a été créé avec succès !")
            return redirect("connecter_compte")
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = InscriptionForm()

    return render(request, "utilisateurs/inscription.html", {"form": form})
