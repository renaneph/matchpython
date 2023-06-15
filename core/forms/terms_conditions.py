from django import forms
from core.models.terms_conditions import TermsConditions


class TermsConditionsForm(forms.ModelForm):
    class Meta:
        model = TermsConditions
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "upload_termsconditions": forms.FileInput(attrs={"class": "form-control", "accept": ".pdf"})
        }
