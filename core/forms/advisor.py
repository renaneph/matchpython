from django import forms

from core.models.advisor import AdvisorUser, FRACTIONAL_C_LEVEL
from core.models.auxiliary_tables import Region, CLevel, CompanyIndustry, CompanyDomain


class ClearableFileInputCustom(forms.ClearableFileInput):
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['is_initial'] = False
        return context

class AdvisorForm(forms.ModelForm):
    fractional_c_level = forms.TypedChoiceField(
        required=True,
        choices=FRACTIONAL_C_LEVEL,
        widget=forms.RadioSelect(
            attrs={"class": "form-check form-check-inline"}
        )
    )

    class Meta:
        model = AdvisorUser
        exclude = ["user_id"]
        widgets = {
            "who_am_I": forms.TextInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "linkedin": forms.TextInput(attrs={"class": "form-control"}),
            "commerce_tech": forms.CheckboxInput(attrs={"class": "form-check form-check-inline"}),
            "fintech": forms.CheckboxInput(attrs={"class": "form-check form-check-inline"}),
            "gtm_strategy": forms.CheckboxInput(attrs={"class": "form-check form-check-inline"}),
            "human_capital": forms.CheckboxInput(attrs={"class": "form-check form-check-inline"}),
            "international": forms.CheckboxInput(attrs={"class": "form-check form-check-inline"}),
            "domestic": forms.CheckboxInput(attrs={"class": "form-check form-check-inline"}),
            "description": forms.Textarea(attrs={"class": "form-control", "cols": 80, "rows": 4}),
            "terms_conditions": forms.CheckboxInput(attrs={"class": "form-check form-check-inline"}),
            "highlight_profile_1": forms.TextInput(attrs={"class": "form-control"}),
            "highlight_profile_2": forms.TextInput(attrs={"class": "form-control"}),
            "highlight_profile_3": forms.TextInput(attrs={"class": "form-control"}),
            "hours_invest": forms.Select(attrs={"class": "form-control"}),
            "start_at": forms.Select(attrs={"class": "form-control"}),
            "upload_resume": forms.FileInput(attrs={
                "class": "form-control",
                "accept": "application/pdf"
            }),
            "upload_profile_picture": ClearableFileInputCustom(attrs={"class": "form-control"}),
            "enable_match": forms.CheckboxInput(attrs={"class": "form-check"})
        }

    def __init__(self, *args, **kwargs):
        super(AdvisorForm, self).__init__(*args, **kwargs)

        checkbox_fields = {
            "regions_user": Region,
            "regions_international": Region,
            "c_level_user": CLevel,
            "fintech_user": CompanyIndustry,
            "commerce_tech_user": CompanyIndustry
        }

        for item in checkbox_fields:
            self.fields[item].widget = forms.CheckboxSelectMultiple(
                attrs={"class": "form-check form-check-inline"}
            )
            self.fields[item].queryset = checkbox_fields[item].objects.all()

        fintech = CompanyDomain.objects.get(name__iexact="fintech")
        self.fields["fintech_user"].queryset = CompanyIndustry.objects.filter(domain=fintech)

        commerce_tech = CompanyDomain.objects.get(name__iexact="commerce tech")
        self.fields["commerce_tech_user"].queryset = CompanyIndustry.objects.filter(domain=commerce_tech)

        self.fields['terms_conditions'].required = True

    def save(self, commit=False, user=None):
        self.instance.who_am_I = "Advisor"
        self.instance.user_id = user
        advisor = super(AdvisorForm, self).save()

        region_list = self.cleaned_data["regions_user"]
        advisor.regions_user.add(*region_list)

        international_list = self.cleaned_data["regions_international"]
        advisor.regions_international.add(*international_list)

        c_level_list = self.cleaned_data["c_level_user"]
        advisor.c_level_user.add(*c_level_list)

        commerce_tech_list = self.cleaned_data["commerce_tech_user"]
        advisor.commerce_tech_user.add(*commerce_tech_list)

        fintech_list = self.cleaned_data["fintech_user"]
        advisor.fintech_user.add(*fintech_list)

        if commit:
            advisor.save()

        return advisor
