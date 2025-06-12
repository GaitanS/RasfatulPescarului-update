from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Lake, UserProfile, FishSpecies, Facility, County, LakePhoto


class CustomUserCreationForm(UserCreationForm):
    """Custom user registration form with additional fields"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Adresa dvs. de email'
        }),
        label="Email*"
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Prenumele dvs.'
        }),
        label="Prenume*"
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Numele dvs. de familie'
        }),
        label="Nume*"
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Numele de utilizator'
        })
        self.fields['username'].label = "Nume utilizator*"
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Parola'
        })
        self.fields['password1'].label = "Parolă*"
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirmați parola'
        })
        self.fields['password2'].label = "Confirmă parola*"

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Un utilizator cu această adresă de email există deja.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            # Create user profile
            UserProfile.objects.create(user=user)
        return user


class CustomAuthenticationForm(AuthenticationForm):
    """Custom login form with Bootstrap styling"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Nume utilizator sau email'
        })
        self.fields['username'].label = "Nume utilizator"
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Parola'
        })
        self.fields['password'].label = "Parolă"


class UserProfileForm(forms.ModelForm):
    """Form for editing user profile"""
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Prenumele dvs.'
        }),
        label="Prenume*"
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Numele dvs. de familie'
        }),
        label="Nume*"
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Adresa dvs. de email'
        }),
        label="Email*"
    )

    class Meta:
        model = UserProfile
        fields = ['phone', 'city', 'county', 'bio', 'avatar']
        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Numărul dvs. de telefon'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Orașul în care locuiți'
            }),
            'county': forms.Select(attrs={
                'class': 'form-select'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Scurtă descriere despre dvs. și experiența la pescuit'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }
        labels = {
            'phone': 'Telefon',
            'city': 'Orașul',
            'county': 'Județul',
            'bio': 'Despre mine',
            'avatar': 'Fotografie de profil'
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name
            self.fields['email'].initial = self.user.email

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if self.user and User.objects.filter(email=email).exclude(pk=self.user.pk).exists():
            raise ValidationError("Un utilizator cu această adresă de email există deja.")
        return email

    def save(self, commit=True):
        profile = super().save(commit=False)
        if self.user:
            self.user.first_name = self.cleaned_data['first_name']
            self.user.last_name = self.cleaned_data['last_name']
            self.user.email = self.cleaned_data['email']
            if commit:
                self.user.save()
        if commit:
            profile.save()
        return profile


class LakeForm(forms.ModelForm):
    """Form for creating and editing lakes"""
    
    class Meta:
        model = Lake
        fields = [
            'name', 'description', 'address', 'county', 'latitude', 'longitude',
            'google_maps_embed', 'lake_type', 'fish_species', 'facilities',
            'price_per_day', 'rules', 'contact_phone', 'contact_email',
            'number_of_stands', 'surface_area', 'depth_min', 'depth_max',
            'depth_average', 'length_min', 'length_max', 'width_min', 'width_max',
            'website', 'facebook_url', 'instagram_url'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Numele complet al bălții'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descrierea detaliată a bălții, facilităților și condițiilor de pescuit'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Comuna X, Județul Y'
            }),
            'county': forms.Select(attrs={
                'class': 'form-select'
            }),
            'latitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '45.39189813235069',
                'step': 'any'
            }),
            'longitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '24.62707585690222',
                'step': 'any'
            }),
            'google_maps_embed': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Cod iframe complet de la Google Maps (opțional)'
            }),
            'lake_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'fish_species': forms.CheckboxSelectMultiple(),
            'facilities': forms.CheckboxSelectMultiple(),
            'price_per_day': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '50.00',
                'step': '0.01'
            }),
            'rules': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Regulile și restricțiile pentru pescuitul pe acest lac'
            }),
            'contact_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '0700 123 456'
            }),
            'contact_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'contact@balta.ro'
            }),
            'number_of_stands': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '10'
            }),
            'surface_area': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '2.5',
                'step': '0.01'
            }),
            'depth_min': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '1.0',
                'step': '0.01'
            }),
            'depth_max': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '3.5',
                'step': '0.01'
            }),
            'depth_average': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '2.0',
                'step': '0.01'
            }),
            'length_min': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '100.0',
                'step': '0.01'
            }),
            'length_max': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '200.0',
                'step': '0.01'
            }),
            'width_min': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '50.0',
                'step': '0.01'
            }),
            'width_max': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '80.0',
                'step': '0.01'
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://www.balta.ro'
            }),
            'facebook_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://facebook.com/balta'
            }),
            'instagram_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://instagram.com/balta'
            })
        }
        labels = {
            'name': 'Numele bălții*',
            'description': 'Descriere',
            'address': 'Localitate, județ*',
            'county': 'Județul*',
            'latitude': 'Latitudine*',
            'longitude': 'Longitudine*',
            'google_maps_embed': 'Cod embed Google Maps',
            'lake_type': 'Tipul bălții',
            'fish_species': 'Specii de pești*',
            'facilities': 'Facilități*',
            'price_per_day': 'Prețuri/taxe de pescuit (RON)*',
            'rules': 'Regulament*',
            'contact_phone': 'Telefon*',
            'contact_email': 'Email*',
            'number_of_stands': 'Număr de standuri',
            'surface_area': 'Suprafață (ha)',
            'depth_min': 'Adâncime minimă (m)',
            'depth_max': 'Adâncime maximă (m)',
            'depth_average': 'Adâncime medie (m)',
            'length_min': 'Lungime minimă (m)',
            'length_max': 'Lungime maximă (m)',
            'width_min': 'Lățime minimă (m)',
            'width_max': 'Lățime maximă (m)',
            'website': 'Site web',
            'facebook_url': 'Facebook',
            'instagram_url': 'Instagram'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make required fields more obvious
        required_fields = ['name', 'address', 'county', 'latitude', 'longitude', 
                          'fish_species', 'facilities', 'price_per_day', 'rules',
                          'contact_phone', 'contact_email']
        for field_name in required_fields:
            if field_name in self.fields:
                self.fields[field_name].required = True


class LakePhotoForm(forms.ModelForm):
    """Form for uploading lake photos"""
    
    class Meta:
        model = LakePhoto
        fields = ['image', 'title', 'description', 'is_main']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/jpeg,image/png'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Titlu descriptiv pentru imagine'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descriere detaliată a imaginii'
            }),
            'is_main': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        labels = {
            'image': 'Imagine*',
            'title': 'Titlu imagine',
            'description': 'Descriere imagine',
            'is_main': 'Imagine principală'
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Check file size (max 2MB)
            if image.size > 2 * 1024 * 1024:
                raise ValidationError("Imaginea nu poate fi mai mare de 2MB.")
            
            # Check file type
            if not image.content_type in ['image/jpeg', 'image/png']:
                raise ValidationError("Doar fișierele JPEG și PNG sunt permise.")
        
        return image
