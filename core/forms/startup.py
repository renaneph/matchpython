from django import forms

from core.models.auxiliary_tables import Region, CompanyDomain, CompanyIndustry, CLevel
from core.models.startup import StartupUser, ADMIN_EVENTS


class ClearableFileInputCustom(forms.ClearableFileInput):
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['is_initial'] = False
        return context

class StartupForm(forms.ModelForm):
    admins_events = forms.TypedChoiceField(
        required=True,
        choices=ADMIN_EVENTS,
        widget=forms.RadioSelect(
            attrs={"class": "form-check form-check-inline"}
        )
    )

    class Meta:
        model = StartupUser
        exclude = ["user_id"]
        widgets = {
            "who_am_I": forms.TextInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "position": forms.TextInput(attrs={"class": "form-control"}),
            "company_name": forms.TextInput(attrs={"class": "form-control"}),
            "fintech": forms.CheckboxInput(attrs={"class": "form-check form-check-inline"}),
            "commerce_tech": forms.CheckboxInput(attrs={"class": "form-check form-check-inline"}),
            "gtm_strategy": forms.CheckboxInput(attrs={"class": "form-check form-check-inline"}),
            "fundraising": forms.CheckboxInput(attrs={"class": "form-check form-check-inline"}),
            "tech": forms.CheckboxInput(attrs={"class": "form-check form-check-inline"}),
            "human_capital": forms.CheckboxInput(attrs={"class": "form-check form-check-inline"}),
            "international": forms.CheckboxInput(attrs={"class": "form-check form-check-inline"}),
            "domestic": forms.CheckboxInput(attrs={"class": "form-check form-check-inline"}),
            "company_description": forms.Textarea(attrs={"class": "form-control", "cols": 80, "rows": 4}),
            "describe_help": forms.Textarea(attrs={"class": "form-control", "cols": 80, "rows": 4}),
            "terms_conditions": forms.CheckboxInput(attrs={"class": "form-check form-check-inline"}),
            "problem": forms.Textarea(attrs={"class": "form-control", "cols": 80, "rows": 4}),
            "solution": forms.Textarea(attrs={"class": "form-control", "cols": 80, "rows": 4}),
            "funding_id": forms.Select(attrs={"class": "form-control"}),
            "annual_profit": forms.Select(attrs={"class": "form-control"}),
            "goals": forms.Select(attrs={"class": "form-control"}),
            "upload_deck": forms.FileInput(attrs={
                "class": "form-control",
                "accept": "application/pdf"
            }),
            "upload_profile_picture": ClearableFileInputCustom(attrs={"class": "form-control"}),
            "enable_match": forms.CheckboxInput(attrs={"class": "form-check"}),
            "functions_events": forms.CheckboxInput(attrs={"class": "form-check"})
        }

    def __init__(self, *args, **kwargs):
        super(StartupForm, self).__init__(*args, **kwargs)

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
        self.instance.who_am_I = "Startup"
        self.instance.user_id = user
        startup = super(StartupForm, self).save()

        region_list = self.cleaned_data["regions_user"]
        startup.regions_user.add(*region_list)

        international_list = self.cleaned_data["regions_international"]
        startup.regions_international.add(*international_list)

        c_level_list = self.cleaned_data["c_level_user"]
        startup.c_level_user.add(*c_level_list)

        commerce_tech_list = self.cleaned_data["commerce_tech_user"]
        startup.commerce_tech_user.add(*commerce_tech_list)

        fintech_list = self.cleaned_data["fintech_user"]
        startup.fintech_user.add(*fintech_list)

        c_level_list = self.cleaned_data["c_level_user"]
        startup.c_level_user.add(*c_level_list)

        if commit:
            startup.save()

        return startup
