from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.db.utils import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, resolve_url as r

from core.forms.advisor import AdvisorForm
from core.forms.startup import StartupForm
from user.forms import CustomRegisterForm, CustomChangeForm
from core.views.match import match_list_for_advisor, match_list_for_startup, matches_list_only, \
    no_matches_list_for_user_id, matches_closed, matches_interest_expressed
from core.views.interest_expressed import interest_expressed
from core.models.advisor import AdvisorUser
from core.models.startup import StartupUser
from core.models.testimonials import Testimonials
from core.forms.interest_expressed import InterestExpressedForm
from core.models.terms_conditions import TermsConditions
from core.models.testimonials import Testimonials
from core.views.match import match_list_for_advisor, match_list_for_startup, matches_list_only, \
    no_matches_list_for_user_id
from user.forms import CustomRegisterForm, CustomChangeForm, RegisterAdminForm

User = get_user_model()


@login_required()
def admin(request):
    user_form = CustomRegisterForm(instance=request.user)

    if request.user.is_staff:
        matches_context = matches_list_only(request)
        form = {"who_am_I": "Admin"}
        context = {
            "user_form": user_form,
            "form": form,
            "matches_list": matches_context["matches"],
            "advisors": matches_context["advisors"],
            "startups": matches_context["startups"],
            "matches_closed_list": matches_closed(request),
            "matches_interest_expressed_list": matches_interest_expressed(request),
            "interest_expressed_list": interest_expressed(request),
        }
    else:
        try:
            user = AdvisorUser.objects.get(user_id=request.user.id)
            form = AdvisorForm(instance=user)
            matches_list = match_list_for_advisor(request)
        except ObjectDoesNotExist:
            user = StartupUser.objects.get(user_id=request.user.id)
            form = StartupForm(instance=user)
            matches_list = match_list_for_startup(request)

        no_matches_list = no_matches_list_for_user_id(user)

        interest_expressed_form = InterestExpressedForm()

        context = {
            "user_form": user_form,
            "form": form,
            "matches_list": matches_list,
            "no_matches_list": no_matches_list,
            "interest_expressed_form": interest_expressed_form
        }

        if user.status == 4:
            context['matches_list'] = []
            messages.error(request, 'User Inactive')

    return render(request, 'user/home_admin_dashboard.html', context)


def home(request):
    user_form = CustomRegisterForm(request.POST or None)
    form_startup = StartupForm(request.POST or None)
    form_advisor = AdvisorForm(request.POST or None)
    testimonials = Testimonials.objects.all()
    terms_condition_actual = TermsConditions.objects.last()

    context = {
        "user_form": user_form,
        "form_startup": form_startup,
        "form_advisor": form_advisor,
        "testimonials": testimonials,
        "terms_conditions": terms_condition_actual,
    }
    return render(request, 'home.html', context)


@login_required()
def about(request):
    if request.method == "GET":
        return render(request, 'about.html')


@login_required()
def user_list(request):
    if not request.user.is_active and request.user.is_staff:
        raise PermissionDenied

    if request.method == "GET":
        users = User.objects.filter(is_staff=True).filter(is_active=True)
        data = {
            'user_list': users
        }
        return render(request, 'user/users_list.html', data)


@login_required()
def users_delete(request, pk):
    if not request.user.is_active and request.user.is_staff:
        raise PermissionDenied

    admin_user = get_object_or_404(User, pk=pk)

    if request.user == admin_user:
        messages.error(request, "You cannot remove this registry. ")
        return HttpResponseRedirect(r("user:list"))

    if request.method == 'POST':
        admin_user.is_active = False
        admin_user.save()
        messages.success(request, "Registry removed successfully")
        return HttpResponseRedirect(r("user:list"))


@login_required()
def users_edit(request, pk):
    if not request.user.is_active and request.user.is_staff:
        raise PermissionDenied

    django_user = get_object_or_404(User, pk=pk)
    admin_user_form = RegisterAdminForm(instance=django_user.adminuser)
    django_user_form = CustomChangeForm(instance=django_user)

    if request.method == "POST":
        admin_user_form = RegisterAdminForm(request.POST, request.FILES, instance=django_user.adminuser)
        django_user_form = CustomChangeForm(request.POST, instance=django_user)

        if admin_user_form.is_valid() and django_user_form.is_valid():

            user = django_user_form.save()
            admin_user_form.save(user=user)

            messages.success(request, "Admin Updated successfully")
            return HttpResponseRedirect(r("user:list"))

    context = {
        "django_user_form": django_user_form,
        "admin_user_form": admin_user_form
    }
    return render(request, 'user/user_form.html', context)


@login_required()
def users_register(request):
    if not request.user.is_active and request.user.is_staff:
        raise PermissionDenied

    django_user_form = CustomRegisterForm()
    admin_user_form = RegisterAdminForm()

    if request.method == "POST":
        django_user_form = CustomRegisterForm(request.POST)
        admin_user_form = RegisterAdminForm(request.POST, request.FILES)

        if django_user_form.is_valid() and admin_user_form.is_valid():
            try:
                django_user = django_user_form.save(who_am_i="Admin")
                admin_user_form.save(user=django_user)

                messages.success(request, "Registry added successfully")
                return HttpResponseRedirect(r("user:list"))

            except IntegrityError:
                messages.error(request, "This email is already in use!")

    context = {
        "django_user_form": django_user_form,
        "admin_user_form": admin_user_form,
        "new": True
    }
    return render(request, 'user/user_form.html', context)
