from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import InscriptionForm, AbonnementForm,ConnectionForm,ProfilFormfrom, TestCompatibiliteForm

from django.contrib.auth import logout, authenticate, login

# Create your views here.

def index(request):
    form = ConnectionForm()
    return render(request, "utilisateurs/connecter_compte.html", {"form": form})

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
<<<<<<< .mine

=======

>>>>>>> .theirs

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
    if request.method == "POST":
        form = ConnectionForm(request.POST)
        if form.is_valid():
            try:
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]
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
        



