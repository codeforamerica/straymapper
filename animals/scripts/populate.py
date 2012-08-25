import os
import csv
from datetime import datetime, date
from geopy import geocoders

from animals.models import Animal
from animals.tasks import populate


def run():
    csv_file = open("%s/../fixtures/straydata-8-24-2012-5-00-13-PM.csv" % os.path.dirname(__file__))
    contents = csv.reader(csv_file, dialect='excel', delimiter=',')
    header = contents.next()
    g = geocoders.Google('AIzaSyAZoNPSlRTETltbmJvgYYqol0SLAVBgKs')
    for row in contents:
        populate.delay(row)
