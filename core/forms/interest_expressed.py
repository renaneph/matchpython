from django import forms
from core.models.interest_expressed import InterestExpressed


class InterestExpressedForm(forms.ModelForm):
    class Meta:
        model = InterestExpressed
        fields = "__all__"
        widgets = {
            "reason_description": forms.Textarea(attrs={"class": "form-control", "cols": 80, "rows": 4}),
            "reason_i_know_one": forms.CheckboxInput(attrs={"class": "form-check"}),
            "reason_i_am_interested": forms.CheckboxInput(attrs={"class": "form-check"}),
            "reason_other": forms.CheckboxInput(attrs={"class": "form-check"}),
        }
