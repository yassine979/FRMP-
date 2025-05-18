from django import forms
from .models import ContactMessage, Profile, CustomUser


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['display_name','profile_picture', 'city', 'country', 'cin', 'date_of_birth']
        widgets = {
            'display_name': forms.TextInput(attrs={'placeholder': 'Display Name', 'class': 'form-control'}),
            'city': forms.TextInput(attrs={'placeholder': 'Ville','class': 'form-control'}),
            'country': forms.TextInput(attrs={'placeholder': 'Pays','class': 'form-control'}),
            'profile_picture': forms.FileInput(),
            'cin': forms.TextInput(attrs={'placeholder': 'CIN','class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }



class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['full_name', 'email', 'phone', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone Number'}),
            'message': forms.Textarea(attrs={'placeholder': 'Message', 'class': 'message_input'}),
        }
