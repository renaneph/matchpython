from django import forms

from core.models.match import MatchFiles

class MatchFilesForm(forms.ModelForm):
    class Meta:
        model = MatchFiles
        fields = ("file", )
        widgets = {
            "file": forms.FileInput(attrs={"class": "form-control"}),
        }