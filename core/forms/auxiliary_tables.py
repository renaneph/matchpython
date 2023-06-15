from django import forms

from core.models.auxiliary_tables import Region, CompanyDomain, CompanyIndustry, Funding, CLevel, MatchKeysPoints


class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "points": forms.NumberInput(attrs={"class": "form-control"})
        }


class CompanyDomainForm(forms.ModelForm):
    class Meta:
        model = CompanyDomain
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
        }


class CompanyIndustryForm(forms.ModelForm):
    class Meta:
        model = CompanyIndustry
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "domain": forms.Select(attrs={"class": "form-control"}),
            "points": forms.NumberInput(attrs={"class": "form-control"})
        }


class FundingForm(forms.ModelForm):
    class Meta:
        model = Funding
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"})
        }


class CLevelForm(forms.ModelForm):
    class Meta:
        model = CLevel
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "points": forms.NumberInput(attrs={"class": "form-control"})
        }


class MatchKeysPointsForm(forms.ModelForm):
    class Meta:
        model = MatchKeysPoints
        fields = "__all__"
        widgets = {
            "gtm_name": forms.TextInput(attrs={"class": "form-control"}),
            "gtm_points": forms.NumberInput(attrs={"class": "form-control"}),
            "tech_name": forms.TextInput(attrs={"class": "form-control"}),
            "tech_points": forms.NumberInput(attrs={"class": "form-control"}),
            "fundraising_name": forms.TextInput(attrs={"class": "form-control"}),
            "fundraising_points": forms.NumberInput(attrs={"class": "form-control"}),
        }
