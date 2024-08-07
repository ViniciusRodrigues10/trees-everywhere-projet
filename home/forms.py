from django import forms
from .models import PlantedTree, Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class PlantedTreeForm(forms.ModelForm):
    """
    Form for adding or updating a PlantedTree instance.
    """

    class Meta:
        model = PlantedTree
        fields = ["tree", "age", "latitude", "longitude", "account"]


class UserRegistrationForm(UserCreationForm):
    """
    Form for user registration, extending Django's UserCreationForm.
    """

    about = forms.CharField(required=False, widget=forms.Textarea)

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "about")

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            Profile.objects.create(user=user, about=self.cleaned_data["about"])
        return user
