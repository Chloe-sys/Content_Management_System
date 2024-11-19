from django import forms
from django.contrib.auth.models import User
from .models import Poster

# Create a registration form
class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirm = forms.CharField(widget=forms.PasswordInput)
    bio = forms.CharField(required=False, widget=forms.Textarea)
    profile_picture = forms.ImageField(required=False)
   

    class Meta:
        model = User
        fields = [ 'bio', 'profile_picture',  'email', 'password', 'username']

def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Set the user's password correctly
        
        if commit:
            user.save()
            # Create UserProfile with additional fields
            profile = User_Profile(user=user)
            profile.bio = self.cleaned_data['bio']
            profile.profile_picture = self.cleaned_data['profile_picture']
            profile.save()
        return user


class PosterRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Poster
        fields = ['username', 'password', 'password_confirm']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match")

    def save(self, commit=True):
        poster = super().save(commit=False)
        poster.set_password(self.cleaned_data["password"])  # Hash the password
        if commit:
            poster.save()
        return poster

class PosterLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
