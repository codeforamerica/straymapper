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
                alist = animal_list.filter(intake_condition=intake_condition)
            intake_date = form.cleaned_data['intake_date']
            if intake_date:
                alist = animal_list.filter(intake_date=intake_date)
            animal_type = form.cleaned_data['animal_type']
            if animal_type:
                alist = animal_list.filter(animal_type=animal_type)
            sex = form.cleaned_data['sex']
            if sex:
                alist = animal_list.filter(sex=sex)
    else:
        form = AnimalSearchForm()
        alist = Animal.objects.all()

    context['form'] = form
    context['animal_list'] = alist
    return render_to_response(template_name, context,
        context_instance=RequestContext(request))
