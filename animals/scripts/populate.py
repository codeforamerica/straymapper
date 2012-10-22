import os
import csv

from animals.models import Animal
from animals.tasks import populate


def run():
    fn = "straydata-9-8-2012-8-15-52-AM.csv"
    csv_file = open("%s/../fixtures/%s" % (os.path.dirname(__file__), fn))
    contents = csv.reader(csv_file, dialect='excel', delimiter=',')
    header = contents.next()
    for index, row in enumerate(contents):
        populate.apply_async(args=[row], countdown=index)
