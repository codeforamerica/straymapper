from django.shortcuts import render_to_response
from django.template import RequestContext

from animals.models import Animal
from animals.forms import AnimalSearchForm

def index(request, template_name='animals/index.html'):
    context = {}

    if request.method == 'POST':
        form = AnimalSearchForm(request.POST)
        animal_list = Animal.objects.all()
    else:
        form = AnimalSearchForm()
        animal_list = Animal.objects.all()

    context['form'] = form
    context['animal_list'] = animal_list
    return render_to_response(template_name, context,
        context_instance=RequestContext(request))
