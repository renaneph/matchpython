from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, resolve_url as r, get_object_or_404, redirect

from core.forms.startup import StartupForm
from core.models.startup import StartupUser
from core.models.terms_conditions import TermsConditions
from core.views.mail import email_admin, email_startup_advisor_register, email_startup_advisor_active
from core.views.match import match_list_for_startup_user_id, format_object
from user.views import home
from user.forms import CustomRegisterForm, CustomChangeForm
from core.tools import count_points

User = get_user_model()

@login_required()
def startup_list(request):
    if not request.user.is_staff:
        raise PermissionDenied

    startup = StartupUser.objects.all()
    context = {"startup": startup}

    return render(request, 'core/startup/startup_list.html', context)


@login_required()
def startup_form(request):
    if not request.user.is_staff:
        raise PermissionDenied

    user_form = CustomRegisterForm(request.POST or None)
    form = StartupForm(request.POST, request.FILES or None)
    terms_condition_actual = TermsConditions.objects.last()

    if request.method == "POST":

        if user_form.is_valid() and form.is_valid():
            try:
                django_user = user_form.save()
                form.save(user=django_user)

                messages.success(request, "Registry added successfully")
                return HttpResponseRedirect(r("core:startup_list"))

            except IntegrityError:
                messages.error(request, "This email is already in use!")

    context = {
        "user_form": user_form,
        "form": form,
        "new": True,
        "terms_conditions": terms_condition_actual,
    }
    return render(request, "core/startup/startup_form.html", context)


def startup_form_home(request):

    user_form = CustomRegisterForm(request.POST or None)
    form = StartupForm(request.POST, request.FILES or None)

    if request.method == "POST":
        if user_form.is_valid() and form.is_valid():
            try:
                django_user = user_form.save()
                startup = form.save(user=django_user)

                formated_match_keys = format_object(startup)
                
                count = count_points.countPoints(formated_match_keys)

                email_admin(
                    host=str(request.get_host()),
                    user_profile=startup,
                    subject="New startup registration",
                    cause="registration",
                    who_am_i=startup.who_am_I.lower()
                )
                email_startup_advisor_register(user_email=django_user.email)

                startup = form.save(commit=False, user=django_user)
                startup.status = 1
                startup.score = count
                startup.save()

                messages.success(request, "Your submit is successfully")
                return HttpResponseRedirect(r("home"))
            except IntegrityError:
                messages.error(request, "This email is already in use!")
        else:
            messages.error(request, user_form.errors)

    return redirect("/")


@login_required()
def startup_edit(request, pk):
    if not request.user.is_staff:
        raise PermissionDenied

    startup = get_object_or_404(StartupUser, pk=pk)
    form = StartupForm(instance=startup)
    user_form = CustomChangeForm(request.POST or None, instance=startup.user_id)
    terms_condition_actual = TermsConditions.objects.last()

    if request.method == "POST":
        form = StartupForm(request.POST, request.FILES, instance=startup)

        if user_form.is_valid() and form.is_valid():
            try:

                formated_match_keys = format_object(startup)
                count = count_points.countPoints(formated_match_keys)

                django_user = user_form.save()

                startup_id = form.save(commit=False, user=django_user)
                startup_id.score = count
                startup_id.save()

                messages.success(request, "Startup Updated successfully")

                if startup_id.status == 2:
                    email_startup_advisor_active(
                        user_email=django_user.email,
                        host=str(request.get_host())
                    )

                return HttpResponseRedirect(r("core:startup_list"))

            except IntegrityError:
                messages.error(request, "This email is already in use!")

    context = {
        "form": form,
        "user_form": user_form,
        "terms_conditions": terms_condition_actual,
    }

    return render(request, "core/startup/startup_form.html", context)


@login_required()
def startup_edit_from_home(request, pk):

    if request.method == 'GET':
        return HttpResponseRedirect(r("admin"))

    startup = get_object_or_404(StartupUser, pk=pk)
    if not request.user == startup.user_id:
        raise PermissionDenied

    form = StartupForm(request.POST, request.FILES, instance=startup)
    user_form = CustomChangeForm(request.POST or None, instance=startup.user_id)
    terms_condition_actual = TermsConditions.objects.last()

    if request.method == "POST":

        if startup.status == 4:
            return HttpResponseRedirect(r("admin"))
        
        if user_form.is_valid() and form.is_valid():
            try:
                formated_match_keys = format_object(startup)
                count = count_points.countPoints(formated_match_keys)
                
                django_user = user_form.save()
                
                startup.status = 3

                startup_id = form.save(commit=False, user=django_user) 
                startup_id.score = count
                startup_id.save()

                email_admin(
                    host=str(request.get_host()),
                    user_profile=startup,
                    subject="Startup profile edit",
                    cause="update",
                    who_am_i=startup.who_am_I.lower()
                )

                messages.success(request, "Startup Updated successfully")
                return HttpResponseRedirect(r("admin"))

            except IntegrityError:
                messages.error(request, "This email is already in use!")

    context = {
        "form": form,
        "user_form": user_form,
        "terms_conditions": terms_condition_actual,
        "matches_list": match_list_for_startup_user_id(request.user.id)
    }

    if startup.status == 4:
        context['matches_list'] = []
        messages.error(request, 'User Inactive')

    return render(request, 'user/home_admin_dashboard.html', context)


@login_required()
def startup_delete(request, pk):
    if not request.user.is_staff:
        raise PermissionDenied

    startup = get_object_or_404(StartupUser, pk=pk)

    if request.method == 'POST':
        startup.delete()
        messages.success(request, "Registry removed successfully")
        return HttpResponseRedirect(r('core:startup_list'))

    context = {'object': startup}
    return render(request, 'core/delete.html', context)
