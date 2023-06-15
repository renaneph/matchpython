from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render, resolve_url as r, get_object_or_404
from core.tools import update_points

from core.forms.auxiliary_tables import CompanyIndustryForm
from core.models.auxiliary_tables import CompanyIndustry


@login_required()
def company_industry_list(request):
    if not request.user.is_staff:
        raise PermissionDenied

    company_industry = CompanyIndustry.objects.all()
    context = {"company_industry": company_industry}
    return render(request, 'core/company_industry/company_industry_list.html', context)


@login_required()
def company_industry_form(request):
    if not request.user.is_staff:
        raise PermissionDenied

    form = CompanyIndustryForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Registry added successfully")
            return HttpResponseRedirect(r("core:company_industry_list"))

    context = {
        "form": form,
        "new": True
    }
    return render(request, "core/company_industry/company_industry_form.html", context)


@login_required()
def company_industry_edit(request, pk):
    if not request.user.is_staff:
        raise PermissionDenied

    company_industry = get_object_or_404(CompanyIndustry, pk=pk)
    form = CompanyIndustryForm(instance=company_industry)

    if request.method == "POST":
        form = CompanyIndustryForm(request.POST, instance=company_industry)
        if form.is_valid():
            form.save()
            update_points.updatePoints()
            messages.success(request, "Registry updated successfully")
            return HttpResponseRedirect(r("core:company_industry_list"))

    context = {"form": form}
    return render(request, "core/company_industry/company_industry_form.html", context)


@login_required()
def company_industry_delete(request, pk):
    if not request.user.is_staff:
        raise PermissionDenied

    company_industry = get_object_or_404(CompanyIndustry, pk=pk)

    if request.method == 'POST':
        company_industry.delete()
        messages.success(request, "Registry removed successfully")
        return HttpResponseRedirect(r('core:company_industry_list'))

    context = {'object': company_industry}
    return render(request, 'core/delete.html', context)
