from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render, resolve_url as r, get_object_or_404

from core.forms.auxiliary_tables import CompanyDomainForm
from core.models.auxiliary_tables import CompanyDomain


@login_required()
def company_domain_list(request):
    if not request.user.is_staff:
        raise PermissionDenied

    company_domain = CompanyDomain.objects.all()
    context = {"company_domain": company_domain}
    return render(request, 'core/company_domain/company_domain_list.html', context)


@login_required()
def company_domain_form(request):
    if not request.user.is_staff:
        raise PermissionDenied

    form = CompanyDomainForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Registry added successfully")
            return HttpResponseRedirect(r("core:company_domain_list"))

    context = {
        "form": form,
        "new": True
    }
    return render(request, "core/company_domain/company_domain_form.html", context)


@login_required()
def company_domain_edit(request, pk):
    if not request.user.is_staff:
        raise PermissionDenied

    company_domain = get_object_or_404(CompanyDomain, pk=pk)
    form = CompanyDomainForm(instance=company_domain)

    if request.method == "POST":
        form = CompanyDomainForm(request.POST, instance=company_domain)
        if form.is_valid():
            form.save()
            messages.success(request, "Registry updated successfully")
            return HttpResponseRedirect(r("core:company_domain_list"))

    context = {"form": form}
    return render(request, "core/company_domain/company_domain_form.html", context)


@login_required()
def company_domain_delete(request, pk):
    if not request.user.is_staff:
        raise PermissionDenied

    company_domain = get_object_or_404(CompanyDomain, pk=pk)

    if request.method == 'POST':
        company_domain.delete()
        messages.success(request, "Registry removed successfully")
        return HttpResponseRedirect(r('core:company_domain_list'))

    context = {'object': company_domain}
    return render(request, 'core/delete.html', context)
