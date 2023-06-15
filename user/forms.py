from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import widgets, ModelForm, TextInput

from core.forms.advisor import ClearableFileInputCustom
from user.models import AdminUser

User = get_user_model()


class CustomRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].widget = widgets.TextInput(attrs={"class": "form-control"})
        self.fields["last_name"].widget = widgets.TextInput(attrs={"class": "form-control"})
        self.fields["email"].widget = widgets.EmailInput(attrs={"class": "form-control"})
        self.fields['password1'].widget = widgets.PasswordInput(attrs={"class": "form-control"})
        self.fields['password2'].widget = widgets.PasswordInput(attrs={"class": "form-control"})
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True
        self.fields["email"].required = True

    def save(self, commit=True, who_am_i=None):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]
        if who_am_i == "Admin":
            user.is_staff = True
        user.save()
        return user


class CustomChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].widget = widgets.TextInput(attrs={"class": "form-control"})
        self.fields["last_name"].widget = widgets.TextInput(attrs={"class": "form-control"})
        self.fields["email"].widget = widgets.EmailInput(attrs={"class": "form-control"})
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True
        self.fields["email"].required = True

    def save(self, commit=True):
        try:

            this = User.objects.get(id=self.instance.id)
            user = super().save(commit=False)

            if this.first_name != self.instance.first_name:
                user.first_name = self.cleaned_data["first_name"]

            if this.last_name != self.instance.last_name:
                user.last_name = self.cleaned_data["last_name"]

            if this.email != self.instance.email:
                user.email = self.cleaned_data["email"]
                user.username = self.cleaned_data["email"]

                if EmailAddress.objects.filter(user=this, verified=True).exists():
                    old_email_login = EmailAddress.objects.get(user=this)
                    old_email_login.delete()

            user.save()

            return user

        except Exception as e:
            print(e)
            pass


class RegisterAdminForm(ModelForm):
    class Meta:
        model = AdminUser
        exclude = ["user_id", "who_am_I", "permissions"]
        widgets = {
            "position": TextInput(attrs={"class": "form-control"}),
            "upload_profile_picture": ClearableFileInputCustom(attrs={"class": "form-control"}),
        }

    def save(self, commit=False, user=None):

        self.instance.user_id = user
        advisor = super(RegisterAdminForm, self).save()

        if commit:
            advisor.save()

        return advisor
