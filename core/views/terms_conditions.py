from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render, resolve_url as r, get_object_or_404
from core.forms.terms_conditions import TermsConditionsForm
from core.models.terms_conditions import TermsConditions


@login_required()
def termsconditions_list(request):
    if not request.user.is_staff:
        raise PermissionDenied

    terms_conditions = TermsConditions.objects.all()
    context = {"terms_conditions": terms_conditions}
    return render(request, 'core/terms_conditions/termsconditions_list.html', context)


@login_required()
def termsconditions_form(request):
    if not request.user.is_staff:
        raise PermissionDenied

    form = TermsConditionsForm(request.POST, request.FILES or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Registry added successfully")
            return HttpResponseRedirect(r("core:termsconditions_list"))

    context = {
        "form": form,
        "new": True
    }
    return render(request, "core/terms_conditions/termsconditions_form.html", context)


@login_required()
def termsconditions_edit(request, pk):
    if not request.user.is_staff:
        raise PermissionDenied

    termsconditions = get_object_or_404(TermsConditions, pk=pk)
    form = TermsConditionsForm(instance=termsconditions)

    if request.method == "POST":
        form = TermsConditionsForm(request.POST, request.FILES, instance=termsconditions)
        if form.is_valid():
            form.save()
            messages.success(request, "Registry updated successfully")
            return HttpResponseRedirect(r("core:termsconditions_list"))

    context = {"form": form}
    return render(request, "core/terms_conditions/termsconditions_form.html", context)


@login_required()
def termsconditions_delete(request, pk):
    if not request.user.is_staff:
        raise PermissionDenied

    termsconditions = get_object_or_404(TermsConditions, pk=pk)

    if request.method == 'POST':
        termsconditions.delete()
        messages.success(request, "Registry removed successfully")
        return HttpResponseRedirect(r('core:termsconditions_list'))

    context = {'object': termsconditions}
    return render(request, 'core/delete.html', context)
