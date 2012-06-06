import os
import csv
from datetime import datetime, date
from geopy import geocoders

from animals.models import Animal

def run():
    contents = csv.reader(open("%s/../fixtures/CurrentMap.csv" % os.path.dirname(__file__)), dialect='excel', delimiter=',')
    header = contents.next()
    g = geocoders.Google('AIzaSyAZoNPSlRTETltbmJvgYYqol0SLAVBgKs')
    for row in contents:
        animal_id = row[9]
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
                dt = datetime.strptime(intake_date.split(' ')[0], "%m/%d/%Y")
                a.intake_date = date(year=dt.year, month=dt.month, day=dt.day)
                a.location = location
                a.intake_condition = row[2]
                a.animal_type = row[3]
                a.sex = row[4]
                age = row[5]
                a.age = 100
                a.color = row[6]
                a.breed = row[7]
                a.intake_total = int(row[8])
                a.geometry = "POINT (%s %s)" % (point[1], point[0])
                a.save()
                print a
