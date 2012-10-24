from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from .forms import ReportForm
from .models import Report

def index(request, template_name='reports/index.html'):
    context = {}
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
    else:
        form = ReportForm()
    if form.is_valid():
        report = form.save()
        return HttpResponseRedirect(report.get_absolute_url())
    context['form'] = form
    return render(request, template_name, context)

def view(request, id=None, template_name='reports/view.html'):
    context = {}
    context['report'] = get_object_or_404(Report, id=id)
    return render(request, template_name, context)
