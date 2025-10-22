from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Compatibilite
from .forms import InscriptionForm, ProfilForm, TestCompatibiliteForm

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
def test_compatibilite(request, match_id):
    match = get_object_or_404(User, id=match_id)
    
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

            Compatibilite.objects.create(
                utilisateur=request.user,
                match=match,
                score=score_final
            )

            return render(request, "compatibilite_resultat.html", {
                "match": match,
                "score": score_final
            })
    else:
        form = TestCompatibiliteForm()

    return render(request, "compatibilite_form.html", {
        "form": form,
        "match": match
    })
