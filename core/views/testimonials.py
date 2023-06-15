from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render, resolve_url as r, get_object_or_404
from core.forms.testimonials import TestimonialsForm
from core.models.testimonials import Testimonials


@login_required()
def testimonials_list(request):
    if not request.user.is_staff:
        raise PermissionDenied

    testimonials = Testimonials.objects.all()
    context = {"testimonials": testimonials}
    return render(request, 'core/testimonials/testimonials_list.html', context)


@login_required()
def testimonials_form(request):
    if not request.user.is_staff:
        raise PermissionDenied

    form = TestimonialsForm(request.POST, request.FILES or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Registry added successfully")
            return HttpResponseRedirect(r("core:testimonials_list"))

    context = {
        "form": form,
        "new": True
    }
    return render(request, "core/testimonials/testimonials_form.html", context)


@login_required()
def testimonials_edit(request, pk):
    if not request.user.is_staff:
        raise PermissionDenied

    testimonials = get_object_or_404(Testimonials, pk=pk)
    form = TestimonialsForm(instance=testimonials)

    if request.method == "POST":
        form = TestimonialsForm(request.POST, request.FILES, instance=testimonials)
        if form.is_valid():
            form.save()
            messages.success(request, "Registry updated successfully")
            return HttpResponseRedirect(r("core:testimonials_list"))

    context = {"form": form}
    return render(request, "core/testimonials/testimonials_form.html", context)


@login_required()
def testimonials_delete(request, pk):
    if not request.user.is_staff:
        raise PermissionDenied

    testimonials = get_object_or_404(Testimonials, pk=pk)

    if request.method == 'POST':
        testimonials.delete()
        messages.success(request, "Registry removed successfully")
        return HttpResponseRedirect(r('core:testimonials_list'))

    context = {'object': testimonials}
    return render(request, 'core/delete.html', context)
