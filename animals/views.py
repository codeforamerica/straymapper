from django.shortcuts import render_to_response
from django.template import RequestContext
from datetime import datetime, date, timedelta

from animals.models import Animal
from animals.forms import AnimalSearchForm


def index(request, template_name='animals/index.html'):
    context = {}
    #The following line is commented out because we do not have data from 2 weeks ago
    #startdate = datetime.today() - timedelta(days=14)
    startdate = datetime.today() - timedelta(days=24)

    if request.method == 'POST':
        form = AnimalSearchForm(request.POST)
        alist = Animal.objects.all()     

        if form.is_valid():
            intake_condition = form.cleaned_data['intake_condition']
            if intake_condition:
                alist = alist.filter(intake_condition=intake_condition)
            intake_date = form.cleaned_data['intake_date']
            if intake_date:
                alist = alist.filter(intake_date=intake_date)
            animal_type = form.cleaned_data['animal_type']
            if animal_type:
                alist = alist.filter(animal_type=animal_type)
            sex = form.cleaned_data['sex']
            if sex:
                alist = alist.filter(sex=sex)
            alist= alist[:5]
    else:
        form = AnimalSearchForm()
        alist_all = Animal.objects.all()
        alist= alist_all.filter(intake_date__gte=startdate)

    context['form'] = form
    context['alist'] = alist
    
    return render_to_response(template_name, context,
        context_instance=RequestContext(request))
