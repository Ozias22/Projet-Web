from django.shortcuts import render, get_object_or_404

# Create your views here.

def index(request):
    return render(request, "utilisateurs/index.html")

def connexion(request):
    return render(request, "utilisateurs/connecter_compte.html")