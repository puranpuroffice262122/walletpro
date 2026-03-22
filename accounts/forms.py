from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email Address'}))
    phone = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'placeholder': 'Phone Number'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email Address', 'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

class OpenAccountForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['upi_id', 'id_photo', 'address', 'city', 'state', 'pincode']
        widgets = {
            'upi_id': forms.TextInput(attrs={'placeholder': 'yourname@upi'}),
            'address': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Your address'}),
            'city': forms.TextInput(attrs={'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'placeholder': 'State'}),
            'pincode': forms.TextInput(attrs={'placeholder': 'Pincode'}),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'upi_id', 'profile_photo', 'address', 'city', 'state', 'pincode']
