from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render, resolve_url as r, get_object_or_404
from core.tools import update_points

from core.forms.auxiliary_tables import RegionForm
from core.models.auxiliary_tables import Region


@login_required()
def region_list(request):
    if not request.user.is_staff:
        raise PermissionDenied

    regions = Region.objects.all()
    context = {"regions": regions}
    return render(request, 'core/region/region_list.html', context)


@login_required()
def region_form(request):
    if not request.user.is_staff:
        raise PermissionDenied

    form = RegionForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Registry added successfully")
            return HttpResponseRedirect(r("core:region_list"))

    context = {
        "form": form,
        "new": True
    }
    return render(request, "core/region/region_form.html", context)


@login_required()
def region_edit(request, pk):
    if not request.user.is_staff:
        raise PermissionDenied

    region = get_object_or_404(Region, pk=pk)
    form = RegionForm(instance=region)

    if request.method == "POST":
        form = RegionForm(request.POST, instance=region)
        if form.is_valid():
            form.save()
            update_points.updatePoints()
            messages.success(request, "Registry updated successfully")
            return HttpResponseRedirect(r("core:region_list"))

    context = {"form": form}
    return render(request, "core/region/region_form.html", context)


@login_required()
def region_delete(request, pk):
    if not request.user.is_staff:
        raise PermissionDenied

    region = get_object_or_404(Region, pk=pk)

    if request.method == 'POST':
        region.delete()
        messages.success(request, "Registry removed successfully")
        return HttpResponseRedirect(r('core:region_list'))

    context = {'object': region}
    return render(request, 'core/delete.html', context)
