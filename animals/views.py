from django.db.models import Q
from django.shortcuts import render_to_response
from django.template import RequestContext
from datetime import datetime, date, timedelta

from animals.models import Animal
from animals.forms import AnimalSearchForm


def index(request, template_name='animals/index.html'):
    context = {}
    startdate = datetime.today() - timedelta(days=14)

    if request.method == 'POST':
        form = AnimalSearchForm(request.POST)
        alist = Animal.objects.all()

        if form.is_valid():
            intake_condition = form.cleaned_data['intake_condition']
            if intake_condition:
                alist = alist.filter(intake_condition=intake_condition)
            intake_date_start = form.cleaned_data['intake_date_start']
            intake_date_end = form.cleaned_data['intake_date_end']
            if intake_date_start and intake_date_end:
                alist = alist.filter(intake_date__gte=intake_date_start, 
                                     intake_date__lte=intake_date_end)
            elif intake_date_start: 
                alist = alist.filter(intake_date__gte=intake_date_start) 
            elif intake_date_end: 
                alist = alist.filter(intake_date__lte=intake_date_end)
            animal_type = form.cleaned_data['animal_type']
            if animal_type:
                alist = alist.filter(animal_type=animal_type)
            sex = form.cleaned_data['sex']
            if sex:
                if sex == 'M':
                    alist = alist.filter(Q(sex='M') | Q(sex='N'))
                elif sex == 'F':
                    alist = alist.filter(Q(sex='F') | Q(sex='S'))
    else:
        form = AnimalSearchForm()
        alist_all = Animal.objects.all()
        alist = alist_all.filter(intake_date__gte=startdate)

    context['form'] = form
    context['alist'] = alist
    context['results_count'] = alist.count()
    context['startdate'] = startdate;
    return render_to_response(template_name, context,
        context_instance=RequestContext(request))
