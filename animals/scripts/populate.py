import os
import csv
from datetime import datetime, date
from geopy import geocoders

from animals.models import Animal
from animals.tasks import populate


def run():
    filename = "straydata-9-8-2012-8-15-52-AM.csv"
    csv_file = open("%s/../fixtures/%s" % (os.path.dirname(__file__), filename))
    contents = csv.reader(csv_file, dialect='excel', delimiter=',')
    header = contents.next()
    g = geocoders.Google('AIzaSyAZoNPSlRTETltbmJvgYYqol0SLAVBgKs')
    for index, row in enumerate(contents):
        populate.apply_async(args=[row], countdown=index)
