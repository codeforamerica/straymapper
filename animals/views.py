from datetime import datetime, timedelta

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

#from devserver.modules.profile import devserver_profile
from straymapper.helpers import unicode_csv_reader

from .models import Animal
from .forms import AnimalSearchForm
from .tasks import populate


#@devserver_profile(follow=[])
def index(request, template_name='animals/index.html'):
    context = {}
    alist = Animal.objects.filter(
        Q(outcome_type=u'') | Q(outcome_type=u'ADOPTION'))
    startdate = datetime.today() - timedelta(days=44)
    enddate = datetime.today()
    sort_order = '-intake_date'
    has_image = True

    if request.method == 'POST':
        if 'reset-btn' in request.POST:
            form = AnimalSearchForm()
            request.session['post_data'] = {}
        else:
            form = AnimalSearchForm(request.POST)
            request.session['post_data'] = request.POST.copy()
    else:
        post_data = request.session.get('post_data', None)
        if post_data:
            form = AnimalSearchForm(post_data)
        else:
            form = AnimalSearchForm()

    if form.is_valid():
        intake_condition = form.cleaned_data['intake_condition']
        if intake_condition:
            alist = alist.filter(intake_condition=intake_condition)

        animal_type = form.cleaned_data['animal_type']
        if animal_type:
            alist = alist.filter(animal_type=animal_type)

        sex = form.cleaned_data['sex']
        if sex:
            if sex == 'M':
                alist = alist.filter(Q(sex='M') | Q(sex='N'))
            elif sex == 'F':
                alist = alist.filter(Q(sex='F') | Q(sex='S'))

        is_adoptable = form.cleaned_data['is_adoptable']
        if is_adoptable:
            alist = alist.filter(outcome_type=u'ADOPTION')

        intake_date_start = form.cleaned_data['intake_date_start']
        intake_date_end = form.cleaned_data['intake_date_end']
        if intake_date_start:
            startdate = intake_date_start
            sort_order = 'intake_date'
        if intake_date_end:
            enddate = intake_date_end

        has_image = form.cleaned_data['has_image']

    if has_image:
        alist = alist.exclude(photo=u'')

    alist = alist.filter(intake_date__gte=startdate,
                         intake_date__lte=enddate).order_by(sort_order)

    context['form'] = form
    context['alist'] = alist
    context['results_count'] = alist.count()
    context['startdate'] = startdate
    context['enddate'] = enddate
    return render(request, template_name, context)


def view(request, aid=None, template_name="animals/view.html"):
    context = {}
    context['animal'] = get_object_or_404(Animal, animal_id=aid)
    return render(request, template_name, context)


def popup(request, id=None, template_name="animals/popup.html"):
    context = {}
    context['animal'] = get_object_or_404(Animal, id=id)
    return render(request, template_name, context)


@csrf_exempt
def process_data(request):
    if request.method == 'POST':
        sender = request.POST.get('sender')
        recipient = request.POST.get('recipient')
        subject = request.POST.get('subject')

        for key in request.FILES:
            data_file = request.FILES[key]
            contents = unicode_csv_reader(
                data_file, dialect='excel', delimiter=',')
            header = contents.next()
            for index, row in enumerate(contents):
                populate.apply_async(args=[row], countdown=index)
    return HttpResponse('cool')
