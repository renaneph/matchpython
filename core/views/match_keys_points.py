from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render, resolve_url as r, get_object_or_404

from core.forms.auxiliary_tables import MatchKeysPointsForm
from core.models.auxiliary_tables import MatchKeysPoints
from core.tools import update_points

@login_required()
def match_keys_points_edit(request):
    if not request.user.is_staff:
        raise PermissionDenied

#    match_keys_points = get_object_or_404(MatchKeysPoints, pk=1)
    match_keys_points_list = MatchKeysPoints.objects.all()
    match_keys_points = MatchKeysPoints()
    if match_keys_points_list:
        match_keys_points = match_keys_points_list[0]
    form = MatchKeysPointsForm(instance=match_keys_points)

    if request.method == "POST":
        form = MatchKeysPointsForm(request.POST, instance=match_keys_points)
        if form.is_valid():
            form.save()
            update_points.updatePoints()
            messages.success(request, "Registry updated successfully")
            return HttpResponseRedirect(r("core:match_keys_points_edit"))

    context = {"form": form}
    return render(request, "core/match_keys_points/match_keys_points_form.html", context)


'''
@login_required()
def match_keys_points_list(request):
    if not request.user.is_staff:
        raise PermissionDenied

    match_keys_points = MatchKeysPoints.objects.all()
    context = {"match_keys_points": match_keys_points}
    return render(request, 'core/match_keys_points/match_keys_points_list.html', context)

@login_required()
def match_keys_points_form(request):
    if not request.user.is_staff:
        raise PermissionDenied

    form = MatchKeysPointsForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Registry added successfully")
            return HttpResponseRedirect(r("core:match_keys_points_list"))

    context = {
        "form": form,
        "new": True
    }
    return render(request, "core/match_keys_points/match_keys_points_form.html", context)


@login_required()
def match_keys_points_edit(request):
    if not request.user.is_staff:
        raise PermissionDenied

#    match_keys_points = get_object_or_404(MatchKeysPoints, pk=1)
    match_keys_points_list = MatchKeysPoints.objects.all()
    match_keys_points = MatchKeysPoints()
    if match_keys_points_list:
        match_keys_points = match_keys_points_list[0]
    form = MatchKeysPointsForm(instance=match_keys_points)

    if request.method == "POST":
        form = MatchKeysPointsForm(request.POST, instance=match_keys_points)
        if form.is_valid():
            form.save()
            messages.success(request, "Registry updated successfully")
            return HttpResponseRedirect(r("core:match_keys_points_list"))

    context = {"form": form}
    return render(request, "core/match_keys_points/match_keys_points_form.html", context)


@login_required()
def match_keys_points_delete(request, pk):
    if not request.user.is_staff:
        raise PermissionDenied

    match_keys_points = get_object_or_404(MatchKeysPoints, pk=pk)

    if request.method == 'POST':
        match_keys_points.delete()
        messages.success(request, "Registry removed successfully")
        return HttpResponseRedirect(r('core:match_keys_points_list'))

    context = {'object': match_keys_points}
    return render(request, 'core/delete.html', context)
'''