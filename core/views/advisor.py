from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, resolve_url as r, get_object_or_404

from core.forms.advisor import AdvisorForm
from core.models.advisor import AdvisorUser
from core.models.terms_conditions import TermsConditions
from core.views.mail import email_admin, email_startup_advisor_register, email_startup_advisor_active
from core.views.match import match_list_for_advisor_user_id, format_object
from user.forms import CustomRegisterForm, CustomChangeForm
from core.tools import count_points

User = get_user_model()


@login_required()
def advisor_list(request):
    if not request.user.is_staff:
        raise PermissionDenied

    advisors = AdvisorUser.objects.all()
    context = {"advisors": advisors}
    return render(request, 'core/advisor/advisor_list.html', context)


@login_required()
def advisor_form(request):
    if not request.user.is_staff:
        raise PermissionDenied

    user_form = CustomRegisterForm(request.POST or None)
    form = AdvisorForm(request.POST, request.FILES or None)
    terms_condition_actual = TermsConditions.objects.last()

    if request.method == "POST":

        if user_form.is_valid() and form.is_valid():
            try:
                django_user = user_form.save()
                form.save(user=django_user)

                messages.success(request, "Registry added successfully")
                return HttpResponseRedirect(r("core:advisor_list"))

            except IntegrityError:
                messages.error(request, "This email is already in use!")

    context = {
        "user_form": user_form,
        "form": form,
        "new": True,
        "terms_conditions": terms_condition_actual,
    }
    return render(request, "core/advisor/advisor_form.html", context)


def advisor_form_home(request):

    user_form = CustomRegisterForm(request.POST or None)
    form = AdvisorForm(request.POST, request.FILES or None)

    if request.method == "POST":


        if user_form.is_valid() and form.is_valid():
            try:
                django_user = user_form.save()
                advisor = form.save(user=django_user)

                formated_match_keys = format_object(advisor)

                count = count_points.countPoints(formated_match_keys)

                email_admin(
                    host=str(request.get_host()),
                    user_profile=advisor,
                    subject="New advisor registration",
                    cause="registration",
                    who_am_i=advisor.who_am_I.lower()
                )
                email_startup_advisor_register(user_email=django_user.email)

                advisor = form.save(commit=False, user=django_user)
                advisor.status = 1
                advisor.score = count
                advisor.save()

                messages.success(request, "Your submit is successfully")
                return HttpResponseRedirect(r("home"))
            except IntegrityError:
                messages.error(request, "This email is already in use!")
        else:
            messages.error(request, user_form.errors)

    return HttpResponseRedirect(r("home"))


@login_required()
def advisor_edit(request, pk):
    if not request.user.is_staff:
        raise PermissionDenied

    advisor = get_object_or_404(AdvisorUser, pk=pk)
    form = AdvisorForm(instance=advisor)
    user_form = CustomChangeForm(request.POST or None, instance=advisor.user_id)
    terms_condition_actual = TermsConditions.objects.last()

    if request.method == "POST":
        form = AdvisorForm(request.POST, request.FILES, instance=advisor)

        if user_form.is_valid() and form.is_valid():
            try:
                django_user = user_form.save()

                formated_match_keys = format_object(advisor)
                count = count_points.countPoints(formated_match_keys)

                advisor_id = form.save(commit=False, user=django_user)
                advisor_id.score = count
                advisor_id.save()
                messages.success(request, "Advisor Updated successfully")

                if advisor_id.status == 2:
                    email_startup_advisor_active(
                        user_email=django_user.email,
                        host=str(request.get_host())
                    )

                return HttpResponseRedirect(r("core:advisor_list"))

            except IntegrityError:
                messages.error(request, "This email is already in use!")

    context = {
        "form": form,
        "user_form": user_form,
        "terms_conditions": terms_condition_actual,
    }

    return render(request, "core/advisor/advisor_form.html", context)


@login_required()
def advisor_edit_from_home(request, pk):

    if request.method == 'GET':
        return HttpResponseRedirect(r("admin"))

    advisor = get_object_or_404(AdvisorUser, pk=pk)
    if not request.user == advisor.user_id:
        raise PermissionDenied

    form = AdvisorForm(request.POST, request.FILES, instance=advisor)
    user_form = CustomChangeForm(request.POST or None, instance=advisor.user_id)
    terms_condition_actual = TermsConditions.objects.last()

    if request.method == "POST":

        if advisor.status == 4:
            return HttpResponseRedirect(r("admin"))

        if user_form.is_valid() and form.is_valid():
            try:
                formated_match_keys = format_object(advisor)

                count = count_points.countPoints(formated_match_keys)

                django_user = user_form.save()
                advisor.status = 3

                advisor = form.save(commit=False, user=django_user)
                advisor.score = count
                advisor.save()

                email_admin(
                    host=str(request.get_host()),
                    user_profile=advisor,
                    subject="Advisor profile edit",
                    cause="update",
                    who_am_i=advisor.who_am_I.lower()
                )


                messages.success(request, "Advisor Updated successfully")
                return HttpResponseRedirect(r("admin"))

            except IntegrityError:
                messages.error(request, "This email is already in use!")

    context = {
        "form": form,
        "user_form": user_form,
        "terms_conditions": terms_condition_actual,
        "matches_list": match_list_for_advisor_user_id(request.user.id)
    }


    if advisor.status == 4:
        context['matches_list'] = []
        messages.error(request, 'User Inactive')

    return render(request, 'user/home_admin_dashboard.html', context)


@login_required()
def advisor_delete(request, pk):
    if not request.user.is_staff:
        raise PermissionDenied

    advisor = get_object_or_404(AdvisorUser, pk=pk)

    if request.method == 'POST':
        advisor.delete()
        messages.success(request, "Registry removed successfully")
        return HttpResponseRedirect(r('core:advisor_list'))

    context = {'object': advisor}
    return render(request, 'core/delete.html', context)
