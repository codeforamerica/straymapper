from django.shortcuts import render_to_response
from django.template import RequestContext

from animals.models import Animal

def index(request, template_name='animals/index.html'):
  context = {}

  context['animal_list'] = Animal.objects.all()

  return render_to_response(template_name, context,
      context_instance=RequestContext(request))
