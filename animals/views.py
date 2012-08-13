import csv
from datetime import datetime, date, timedelta

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

#from devserver.modules.profile import devserver_profile
from geopy import geocoders

from animals.models import Animal
from animals.forms import AnimalSearchForm


def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
        dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]


def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')


@csrf_exempt
def process_data(request):
    if request.method == 'POST':
        sender = request.POST.get('sender')
        recipient = request.POST.get('recipient')
        subject = request.POST.get('subject')

        for key in request.FILES:
            data_file = request.FILES[key]
            contents = unicode_csv_reader(data_file, dialect='excel',
                delimiter=',')
            header = contents.next()
            g = geocoders.Google('AIzaSyAZoNPSlRTETltbmJvgYYqol0SLAVBgKs')
            for row in contents:
                animal_id = row[3]
                if not Animal.objects.filter(animal_id=animal_id).exists():
                    location = row[1]
                    location_found = True
                    try:
                        (place, point) = g.geocode(location)
                    except:
                        location_found = False
                    if location_found:
                        a = Animal()
                        a.animal_id = animal_id
                        intake_date = row[0]
                        dt = datetime.strptime(intake_date.strip(), "%m/%d/%y")
                        a.intake_date = date(year=dt.year, month=dt.month,
                            day=dt.day)
                        a.location = location
                        a.intake_condition = row[2]
                        a.animal_type = row[4]
                        sex = {'UNKNOWN': 'U',
                                'MALE': 'M',
                                'FEMALE': 'F'}
                        a.sex = sex[row[5]]
                        a.spayed = True if row[6] == 'YES' else False
                        a.name = row[7]
                        a.age = int(float(row[8].replace(',', '')))
                        a.description = row[9]
                        a.intake_total = 1
                        a.geometry = "POINT (%s %s)" % (point[1], point[0])
                        a.photo = ''
                        a.save()
    return HttpResponse('cool')


#@devserver_profile(follow=[])
def index(request, template_name='animals/index.html'):
    context = {}
    alist = Animal.objects.all()
    startdate = datetime.today() - timedelta(days=44)
    enddate = datetime.today()

    if request.method == 'POST':
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

        has_image = form.cleaned_data['has_image']
        if has_image:
            alist = alist.exclude(photo=u'')

        intake_date_start = form.cleaned_data['intake_date_start']
        intake_date_end = form.cleaned_data['intake_date_end']
        if intake_date_start:
            startdate = intake_date_start
        if intake_date_end:
            enddate = intake_date_end

    alist = alist.filter(intake_date__gte=startdate,
                         intake_date__lte=enddate)

    context['form'] = form
    context['alist'] = alist
    context['results_count'] = alist.count()
    context['startdate'] = startdate
    context['enddate'] = enddate
    return render_to_response(template_name, context,
        context_instance=RequestContext(request))
