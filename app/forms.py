from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .models import Feedback

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'password1', 'password2')

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['employee', 'strengths', 'improvement_areas', 'sentiment']

    def __init__(self, *args, **kwargs):
        manager = kwargs.pop('manager', None)
        super().__init__(*args, **kwargs)
        if manager:
            self.fields['employee'].queryset = manager.team_members.all()
