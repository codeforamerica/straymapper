from django.db.models import Q
from django.shortcuts import render_to_response
from django.template import RequestContext

from animals.models import Animal
from animals.forms import AnimalSearchForm


def index(request, template_name='animals/index.html'):
    context = {}

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
                if animal_type == 'M':
                    alist = alist.filter(Q(animal_type='M') | Q(animal_type='N'))
                elif animal_type == 'F':
                    alist = alist.filter(Q(animal_type='F') | Q(animal_type='S'))
            sex = form.cleaned_data['sex']
            if sex:
                alist = alist.filter(sex=sex)
    else:
        form = AnimalSearchForm()
        alist = Animal.objects.all()

    context['form'] = form
    context['alist'] = alist
    return render_to_response(template_name, context,
        context_instance=RequestContext(request))
