from django import forms
from .models import BureauVote, Candidat, Resultat, CentreVote

class BureauSelectForm(forms.Form):
    bureau = forms.ModelChoiceField(
        queryset=BureauVote.objects.all().select_related('centre').order_by('centre__nom', 'numero'),
        label="Sélectionnez un bureau de vote",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class ResultatForm(forms.ModelForm):
    class Meta:
        model = Resultat
        fields = ['nombre_voix']
        widgets = {
            'nombre_voix': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre_voix'].label = ""

class CandidatForm(forms.ModelForm):
    class Meta:
        model = Candidat
        fields = ['numero', 'nom', 'prenom', 'parti', 'photo']
        widgets = {
            'numero': forms.NumberInput(attrs={'class': 'form-control'}),
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'parti': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

class CentreVoteForm(forms.ModelForm):
    class Meta:
        model = CentreVote
        fields = ['nom', 'commune', 'adresse']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'commune': forms.TextInput(attrs={'class': 'form-control'}),
            'adresse': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class BureauVoteForm(forms.ModelForm):
    class Meta:
        model = BureauVote
        fields = ['centre', 'numero', 'nombre_inscrits']
        widgets = {
            'centre': forms.Select(attrs={'class': 'form-control'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_inscrits': forms.NumberInput(attrs={'class': 'form-control'}),
        }
