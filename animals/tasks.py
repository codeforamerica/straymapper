from datetime import datetime, date

from celery import task
from geopy import geocoders

from animals.models import Animal

g = geocoders.Google('AIzaSyAZoNPSlRTETltbmJvgYYqol0SLAVBgKs')


@task()
def populate(row):
    animal_id = row[3]
    image_updated = True if row[13] == 'New Image Available' else False
    print "starting to process  %s" % animal_id
    if not Animal.objects.filter(animal_id=animal_id).exists():
        location = row[1]
        location_found = True
        try:
            (place, point) = g.geocode(location)
        except:
            location_found = False
            print 'location not found'
        if location_found:
            a = Animal()
            a.animal_id = animal_id
            intake_date = row[0]
            dt = datetime.strptime(intake_date.strip(), "%m/%d/%Y")
            a.intake_date = date(year=dt.year, month=dt.month, day=dt.day)
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
            a.outcome_type = row[10]
            outcome_date = row[11]
            if outcome_date:
                odt = datetime.strptime(intake_date.strip(), "%m/%d/%Y")
                a.outcome_date = date(year=odt.year, month=odt.month,
                    day=odt.day)
            a.transferred_to = row[12]
            a.geometry = "POINT (%s %s)" % (point[1], point[0])
            a.photo = ''
            a.save()
            print a
    elif image_updated:
        print 'marking %s as having photo updated' % animal_id
        a = Animal.objects.get(animal_id=animal_id)
        a.photo_updated = image_updated
        a.save()
    return 'finished processing %s' % (animal_id)
