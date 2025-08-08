from django import forms
from .models import Jockey, Racehorse, Race, Participation

class JockeyForm(forms.ModelForm):
    class Meta:
        model = Jockey
        fields = ['name', 'age']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    
class RacehorseForm(forms.ModelForm):
    class Meta:
        model = Racehorse
        fields = ['name', 'age', 'breed']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'breed': forms.TextInput(attrs={'class': 'form-control'}),
        }

class RaceForm(forms.ModelForm):
    class Meta:
        model = Race
        fields = ['name', 'date', 'location', 'track_configuration', 'track_condition', 'classification', 'season', 'track_length', 'track_surface']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'track_configuration': forms.Select(attrs={'class': 'form-control'}),
            'track_condition': forms.Select(attrs={'class': 'form-control'}),
            'classification': forms.Select(attrs={'class': 'form-control'}),
            'season': forms.Select(attrs={'class': 'form-control'}),
            'track_length': forms.NumberInput(attrs={'class': 'form-control'}),
            'track_surface': forms.Select(attrs={'class': 'form-control'}),
        }

class ParticipationForm(forms.ModelForm):
    class Meta:
        model = Participation
        fields = ['racehorse', 'race', 'jockey', 'position']
        widgets = {
            'racehorse': forms.Select(attrs={'class': 'form-control'}),
            'race': forms.Select(attrs={'class': 'form-control'}),
            'jockey': forms.Select(attrs={'class': 'form-control'}),
            'position': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'is_winner': 'Winner'
        }

    def clean(self):
        cleaned_data = super().clean()
        race = cleaned_data.get('race')
        racehorse = cleaned_data.get('racehorse')
        jockey = cleaned_data.get('jockey')

        # Checking for duplicate racehorse entry in the same race
        if race and racehorse and Participation.objects.filter(race=race, racehorse=racehorse).exclude(pk=self.instance.pk).exists():
            self.add_error('racehorse', 'This racehorse is already participating in this race.')

        # Checking for duplicate jockey entry in the same race
        if race and jockey and Participation.objects.filter(race=race, jockey=jockey).exclude(pk=self.instance.pk).exists():
            self.add_error('jockey', 'This jockey is already participating in this race.')

        return cleaned_data
    

