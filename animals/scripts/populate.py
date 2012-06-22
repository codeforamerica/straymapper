import os
import csv
from datetime import datetime, date
from geopy import geocoders

from animals.models import Animal


def run():
    csv_file = open("%s/../fixtures/DataSet1.csv" % os.path.dirname(__file__))
    contents = csv.reader(csv_file, dialect='excel', delimiter=',')
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
                a.geometry = "POINT (%s %s)" % (point[1], point[0])
                a.save()
                print a
