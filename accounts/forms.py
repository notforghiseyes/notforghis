from django import forms
from .models import Profile
        
class ProfileRegistrationForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['image', 'gender']