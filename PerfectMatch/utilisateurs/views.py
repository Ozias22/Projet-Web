from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import InscriptionForm,AbonementForm

# Create your views here.

def index(request):
    form = AbonementForm()
    return render(request, "utilisateurs/abonement.html", {"form": form})

def inscription_view(request):
    if request.method == "POST":
        form = InscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Votre compte a été créé avec succès !")
            return redirect("connecter_compte")
        else:
            messages.add_message(request, messages.ERROR, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = InscriptionForm()

    return render(request, "utilisateurs/inscription.html", {"form": form})


def valider_abonement(request):
    if request.method == "POST":
        form = AbonementForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Votre abonnement a été validé avec succès !")
            return redirect("connecter_compte")
        else:
            messages.add_message(request, messages.ERROR, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = AbonementForm()

    return render(request, "utilisateurs/abonement.html", {"form": form})