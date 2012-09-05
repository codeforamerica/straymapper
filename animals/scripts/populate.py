import os
import csv
from datetime import datetime, date
from geopy import geocoders

from animals.models import Animal
from animals.tasks import populate


def run():
    csv_file = open("%s/../fixtures/straydata-8-26-2012-2-03-42-PM.csv" % os.path.dirname(__file__))
    contents = csv.reader(csv_file, dialect='excel', delimiter=',')
    header = contents.next()
    g = geocoders.Google('AIzaSyAZoNPSlRTETltbmJvgYYqol0SLAVBgKs')
    for index, row in enumerate(contents):
        populate.apply_async(args=[row], countdown=index)
