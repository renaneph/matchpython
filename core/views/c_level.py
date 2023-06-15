from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render, resolve_url as r, get_object_or_404
from core.tools import update_points

from core.forms.auxiliary_tables import CLevelForm
from core.models.auxiliary_tables import CLevel


@login_required()
def c_level_list(request):
    if not request.user.is_staff:
        raise PermissionDenied

    c_level = CLevel.objects.all()
    context = {"c_level": c_level}
    return render(request, 'core/c_level/c_level_list.html', context)


@login_required()
def c_level_form(request):
    if not request.user.is_staff:
        raise PermissionDenied

    form = CLevelForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Registry added successfully")
            return HttpResponseRedirect(r("core:c_level_list"))

    context = {
        "form": form,
        "new": True
    }
    return render(request, "core/c_level/c_level_form.html", context)


@login_required()
def c_level_edit(request, pk):
    if not request.user.is_staff:
        raise PermissionDenied

    c_level = get_object_or_404(CLevel, pk=pk)
    form = CLevelForm(instance=c_level)

    if request.method == "POST":
        form = CLevelForm(request.POST, instance=c_level)
        if form.is_valid():
            form.save()
            update_points.updatePoints()
            messages.success(request, "Registry updated successfully")
            return HttpResponseRedirect(r("core:c_level_list"))

    context = {"form": form}
    return render(request, "core/c_level/c_level_form.html", context)


@login_required()
def c_level_delete(request, pk):
    if not request.user.is_staff:
        raise PermissionDenied

    c_level = get_object_or_404(CLevel, pk=pk)

    if request.method == 'POST':
        c_level.delete()
        messages.success(request, "Registry removed successfully")
        return HttpResponseRedirect(r('core:c_level_list'))

    context = {'object': c_level}
    return render(request, 'core/delete.html', context)
