from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, resolve_url as r, get_object_or_404
from django.contrib.auth.models import User
import json

from core.models.advisor import AdvisorUser
from core.models.startup import StartupUser
from core.models.interest_expressed import InterestExpressed
from core.forms.interest_expressed import InterestExpressedForm

@login_required()
def interest_expressed_form(request):
    if not request.user.is_staff:
        raise PermissionDenied

    form = InterestExpressedForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Registry added successfully")
            return HttpResponseRedirect(r("core:interest_expressed_list"))

    context = {
        "form": form,
        "new": True
    }
    return render(request, "core/interest_expressed/interest_expressed_form.html", context)

@login_required()
def interest_expressed_set(request):
    if not request.user.is_active and request.user.is_staff:
        raise PermissionDenied

    advisor = AdvisorUser.objects.get(user_id=request.user.id)
    startup = StartupUser.objects.get(id=request.POST['id_startup'])
    form = InterestExpressedForm(request.POST)

    try:
        reason_i_know_one = form['reason_i_know_one'].value()
        reason_i_am_interested = form['reason_i_am_interested'].value()
        reason_other = form['reason_other'].value()
        interest, _ = InterestExpressed.objects.update_or_create(
                          advisor=advisor, startup=startup, 
                          reason_i_know_one = reason_i_know_one,
                          reason_i_am_interested = reason_i_am_interested,
                          reason_other = reason_other,
                          reason_description = request.POST['reason_description']
        )

    except Exception as error:
        messages.success(request, "We got some problem... sorry!")
        return HttpResponse(json.dumps({"success": False}), content_type="application/json")

    messages.success(request, "Registry added successfully")
    return HttpResponseRedirect(r('admin'))

@login_required()
def interest_expressed_list(request):
    if not request.user.is_staff:
        raise PermissionDenied
    
    interests_expressed_list = InterestExpressed.objects.all()

    if request.method == "POST":
        messages.success(request, "Completed successfully")

    context = {
        "interests_expressed_list": interests_expressed_list,
    }

    return render(request, 'core/interest_expressed/interest_expressed_list.html', context)

@login_required()
def interest_expressed_edit(request, pk):
    if not request.user.is_staff:
        raise PermissionDenied

    interest_expressed = get_object_or_404(InterestExpressed, pk=pk)
    form = InterestExpressedForm(instance=interest_expressed)

    if request.method == "POST":
        form = InterestExpressedForm(request.POST, instance=interest_expressed)
        if form.is_valid():
            form.save()
            messages.success(request, "Registry updated successfully")
            return HttpResponseRedirect(r("core:interest_expressed_list"))

    context = {"form": form}
    return render(request, "core/interest_expressed/interest_expressed_form.html", context)


@login_required()
def interest_expressed_delete(request, pk):
    if not request.user.is_staff:
        raise PermissionDenied

    interest_expressed = get_object_or_404(InterestExpressed, pk=pk)

    if request.method == 'POST':
        interest_expressed.delete()
        messages.success(request, "Registry removed successfully")
        return HttpResponseRedirect(r('core:interest_expressed_list'))

    context = {'object': interest_expressed}
    return render(request, 'core/delete.html', context)

@login_required()
def interest_expressed(request):
    if not request.user.is_staff:
        raise PermissionDenied
    
    interests_expressed_list = InterestExpressed.objects.all()

    return interests_expressed_list

