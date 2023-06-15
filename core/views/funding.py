from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render, resolve_url as r, get_object_or_404

from core.forms.auxiliary_tables import FundingForm
from core.models.auxiliary_tables import Funding


@login_required()
def funding_list(request):
    if not request.user.is_staff:
        raise PermissionDenied

    fundings = Funding.objects.all()
    context = {"fundings": fundings}
    return render(request, 'core/funding/funding_list.html', context)


@login_required()
def funding_form(request):
    if not request.user.is_staff:
        raise PermissionDenied

    form = FundingForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Registry added successfully")
            return HttpResponseRedirect(r("core:funding_list"))

    context = {
        "form": form,
        "new": True
    }
    return render(request, "core/funding/funding_form.html", context)


@login_required()
def funding_edit(request, pk):
    if not request.user.is_staff:
        raise PermissionDenied

    funding = get_object_or_404(Funding, pk=pk)
    form = FundingForm(instance=funding)

    if request.method == "POST":
        form = FundingForm(request.POST, instance=funding)
        if form.is_valid():
            form.save()
            messages.success(request, "Registry updated successfully")
            return HttpResponseRedirect(r("core:funding_list"))

    context = {"form": form}
    return render(request, "core/funding/funding_form.html", context)


@login_required()
def funding_delete(request, pk):
    if not request.user.is_staff:
        raise PermissionDenied

    funding = get_object_or_404(Funding, pk=pk)

    if request.method == 'POST':
        funding.delete()
        messages.success(request, "Registry removed successfully")
        return HttpResponseRedirect(r('core:funding_list'))

    context = {'object': funding}
    return render(request, 'core/delete.html', context)
