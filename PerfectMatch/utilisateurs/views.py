
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from .forms import InscriptionForm, AbonnementForm,ConnectionForm,ProfilForm,userProfileForm,ImagesUserForm,TestCompatibiliteForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from .models import User, UserProfile, ImagesUser, Compatibilite

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

            # Compatibilité principale
            Compatibilite.objects.update_or_create(
                utilisateur=request.user,
                match=match,
                defaults={'score': score_final}
            )

            # Compatibilité réciproque (facultatif mais recommandé pour le matching)
            Compatibilite.objects.update_or_create(
                utilisateur=match,
                match=request.user,
                defaults={'score': score_final}
            )

            return render(request, "utilisateurs/compatibilite_resultat.html", {
                "match": match,
                "score": score_final
            })
    else:
        form = TestCompatibiliteForm()

    return render(request, "utilisateurs/compatibilite_form.html", {
        "form": form,
        "match": match
    })

@login_required
def mes_matchs(request):
    matchs = Compatibilite.objects.filter(utilisateur=request.user).order_by('-score')
    return render(request, "utilisateurs/liste_matchs.html", {"matchs": matchs})

        

def profil_perfectmatch_view(request):
    """Vue pour afficher le profil PerfectMatch de l'utilisateur connecté"""

    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    imagesUser = ImagesUser.objects.filter(user=user)

    form1 = userProfileForm(instance=user_profile)
    form2 = ImagesUserForm()

    return render(request, "utilisateurs/profilePerfectMatch.html", {"form1": form1, "form2": form2, "ImagesUser": imagesUser})
