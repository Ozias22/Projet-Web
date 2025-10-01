from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import InscriptionForm, ConnectionForm
from .models import User

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
                email = form.cleaned_data["email"]
                password = form.cleaned_data["password"]
                
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None
            
            if user is not None:
                user = user.authenticate(request, username=user.username, password=user.password)
                if not user.is_active:
                    messages.error(request,"Le compte est désactivé")
                else:
                    login(request, user)
                    messages.success(request,"Connexion a été fait avec succès.")
                return redirect('home')
            else:
                form.add_error(None, "Invalid email or password.")
                
                
            return redirect('index')
    else:
        form = ConnectionForm()
    return render(request, "utilisateurs/connecter_compte.html",{'form': form})
                
            
def accueil(request):
    return render(request, "utilisateurs/accueil.html")


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
