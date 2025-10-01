from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import datetime

User = get_user_model()

class ConnectionForm(forms.Form):
    username = forms.CharField(
        label="Nom d'utilisateur",
        # max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={
            'required': "Le nom d'utilisateur est obligatoire.",
            'invalid': "Entrez une nom d'utilisateur valide."
        })
    password = forms.CharField(
        label="Mot de passe",
        max_length=12,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        error_messages={
            'required': 'Le mot de passe est obligatoire.',
            'max_length': 'Le mot de passe possède au maximum 12 caractères.',
        })
    
    class Meta:
        model = User
        fields = ("username","password")
    
    def clean_username(self):
        username = self.cleaned_data.get("username")
        return username
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        try:
            user = User.objects.get(username__iexact=username)
        except User.DoesNotExist:
            raise forms.ValidationError("Nom d'utilisateur ou mot de passe invalide.")

        if not user.check_password(password):
            raise forms.ValidationError("Nom d'utilisateur ou mot de passe invalide.")

        if not user.is_active:
            raise forms.ValidationError("Ce compte est inactif.")

        # self.user = user
        return cleaned_data
    
        

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



class AbonementForm(forms.Form):
    """Permet à un utilisateur de choisir un abonnement"""
    ABONNEMENT_CHOICES = [
        ('mensuel', 'Abonnement Mensuel - 9.99€'),
        ('trimestriel', 'Abonnement Trimestriel - 24.99€'),
        ('annuel', 'Abonnement Annuel - 79.99€'),
    ]
    nom = forms.CharField(
        label="Nom",
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control'}))
    prenom = forms.CharField(
        label="Prénom",
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control'}))
    email = forms.EmailField(
        label="Email",
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control'}))

    abonnement = forms.ChoiceField(
        choices=ABONNEMENT_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input form-control'
        }),
        error_messages={
            'required': "Veuillez sélectionner un type d'abonnement."
        }
    )
    numero_carte = forms.CharField(
        label="Numéro de carte",
        max_length=16,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '1234 5678 9012 3456'
        }),
        error_messages={
            'required': "Le numéro de carte est obligatoire.",
        }
    )
    date_expiration = forms.DateField(
        label="Date d'expiration",
        required=True,
        widget=forms.DateInput(attrs={
            'class': 'form-control'}),
        error_messages={
            'required': "La date d'expiration est obligatoire."
        })
    cvv = forms.CharField(
        label="CVV",
        max_length=4,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '123'
        }),
        error_messages={
            'required': "Le CVV est obligatoire.",
        })

    def clean_numero_carte(self):
        numero_carte = self.cleaned_data.get("numero_carte")
        if not numero_carte.isdigit() or len(numero_carte) != 16:
            raise ValidationError("Le numéro de carte doit contenir 16 chiffres.")
        return numero_carte
    def clean_cvv(self):
        cvv = self.cleaned_data.get("cvv")
        if not cvv.isdigit() or len(cvv) not in [3, 4]:
            raise ValidationError("Le CVV doit contenir 3 ou 4 chiffres.")
        return cvv
    def clean_date_expiration(self):
        date_expiration = self.cleaned_data.get("date_expiration")
        if date_expiration is None:
            raise ValidationError("La date d'expiration est obligatoire.")
        if date_expiration < datetime.date.today():
            raise ValidationError("La date d'expiration ne peut pas être dans le passé.")
        return date_expiration

    def save(self):
        # Logique pour traiter le paiement et enregistrer l'abonnement
        pass

