# так как свой класс профиля, делаем свои формы для профиля

from django import forms
from .models import Profile
#ModelForm --> from djangos models
class ProfileCreationForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude =('user',)
        fields = ('about', 'avatar')