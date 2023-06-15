from django import forms
from core.models.testimonials import Testimonials


class ClearableFileInputCustom(forms.ClearableFileInput):
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['is_initial'] = False
        return context


class TestimonialsForm(forms.ModelForm):
    class Meta:
        model = Testimonials
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.TextInput(attrs={"class": "form-control"}),
            "text": forms.Textarea(attrs={"class": "form-control", "cols": 80, "rows": 4}),
            "upload_profile_picture": ClearableFileInputCustom(attrs={"class": "form-control"})
        }
