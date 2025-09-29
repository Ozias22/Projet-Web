from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import InscriptionForm

# Create your views here.

def index(request):
    return render(request, "utilisateurs/index.html")

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
