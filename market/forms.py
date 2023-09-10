from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,Production
from django.contrib.auth.forms import AuthenticationForm

class SignUpForm(UserCreationForm):
    ROLE_CHOICES = (
        ('farmer', 'Farmer'),
        ('buyer', 'Buyer'),
    )
    
    role_type = forms.ChoiceField(choices=ROLE_CHOICES)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'role_type']

class CustomAuthenticationForm(AuthenticationForm):
    role_type = forms.ChoiceField(choices=[('farmer', 'Farmer'), ('buyer', 'Buyer'), ('supplier', 'Supplier')])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['role_type'].widget.attrs.update({'class': 'form-control'})


class fUpdateProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email','mobile','age','city_village','state','country','bio']
class bUpdateProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email','mobile','age','city_village','state','country','bio']


class ProductionForm(forms.ModelForm):
    class Meta:
        model = Production
        fields = ['crop_name', 'seed_type', 'starting_date', 'crop_status', 'bio_of_crop', 'harvesting_date', 'image']




class ChatForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea)


class MessageForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), max_length=1000)

