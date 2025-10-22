from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import datetime


User = get_user_model()

class InscriptionForm(UserCreationForm):
    """Permet à un nouvel utilisateur de s'incrire et d'avoir accès au site web"""
    last_name = forms.CharField(
        label="Nom",
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nom'
        }),
        error_messages={
            'required': "Le nom est obligatoire.",
        }
    )
    first_name = forms.CharField(
        label="Prénom",
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Prénom'
        }),
        error_messages={
            'required': "Le prénom est obligatoire.",
        }
    )
    username = forms.CharField(
        label="Nom d'utilisateur",
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nom'
        }),
        error_messages={
            'required': "Le nom d'utilisateur est obligatoire.",
            'unique': "Ce nom d'utilisateur existe déjà."
        }
    )
    email = forms.EmailField(
        label="Email",
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'xyz@email.com'
        }),
        error_messages={
            'required': "L'adresse email est obligatoire.",
            'invalid': "Veuillez entrer une adresse email valide."
        }
    )
    birthday = forms.DateField(
        label="Date de naissance",
        required=True,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        error_messages={
            'required': "La date de naissance est obligatoire."
        }
    )
    country = forms.CharField(
        label="Pays",
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Pays'
        }),
        error_messages={
            'required': "Le pays est obligatoire.",
        }
    )

    city = forms.CharField(
        label="Ville",
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ville'
        }),
        error_messages={
            'required': "La ville est obligatoire.",
        }
    )
    password1 = forms.CharField(
        label="Mot de passe",
        max_length=30,
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mot de passe'
        }),
        error_messages={
            'required': "Le mot de passe est obligatoire",
        }
    )
    password2 = forms.CharField(
        label="Confirmation du mot de passe",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmez le mot de passe'
        }),
        error_messages={
            'required': "Veuillez confirmer votre mot de passe."
        }
    )

    class Meta:
        model = User
        fields = ("username","email","first_name","last_name","country","city", "password1", "birthday", "password2")

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise ValidationError("Ce nom d'utilisateur est déjà pris.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Cette adresse email est déjà utilisée.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Les mots de passe ne correspondent pas.")
        return password2
    def clean_birthday(self):
        birthday = self.cleaned_data.get("birthday")
        if birthday is None:
            raise ValidationError("La date de naissance est obligatoire.")
        if birthday > datetime.date.today():
            raise ValidationError("La date de naissance ne peut pas être dans le futur.")
        return birthday

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["username"]
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.pays = self.cleaned_data["pays"]
        user.ville = self.cleaned_data["ville"]
        if commit:
            user.save()
        return user
    
User = get_user_model()

class ProfilForm(forms.ModelForm):
    age = forms.IntegerField(
        label="Âge",
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
    )
 
    class Meta:
        model = User
        fields = [
            'photo_profil', 'first_name', 'last_name',
            'city', 'country', 'email'
        ]
        labels = {
            'photo_profil': "Photo de profil",
            'first_name': "Prénom",
            'last_name': "Nom",
            'city': "Ville",
            'country': "Pays",
            'email': "Email",
        }
        widgets = {
            'photo_profil': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.birthday:
            today = datetime.date.today()
            age = today.year - self.instance.birthday.year - (
                (today.month, today.day) < (self.instance.birthday.month, self.instance.birthday.day)
            )
            self.fields['age'].initial = age


class TestCompatibiliteForm(forms.Form):
    aime_voyager = forms.ChoiceField(
        label="Aimes-tu voyager ?",
        choices=[("oui", "Oui"), ("non", "Non")],
        widget=forms.RadioSelect
    )
    animal = forms.ChoiceField(
        label="Aimes-tu les animaux ?",
        choices=[("oui", "Oui"), ("non", "Non")],
        widget=forms.RadioSelect
    )
    sport = forms.ChoiceField(
        label="Fais-tu souvent du sport ?",
        choices=[("oui", "Oui"), ("non", "Non")],
        widget=forms.RadioSelect
    )
    fumeur = forms.ChoiceField(
        label="Es-tu fumeur/fumeuse ?",
        choices=[("oui", "Oui"), ("non", "Non")],
        widget=forms.RadioSelect
    )
    musique = forms.ChoiceField(
        label="La musique est-elle importante pour toi ?",
        choices=[("oui", "Oui"), ("non", "Non")],
        widget=forms.RadioSelect
    )