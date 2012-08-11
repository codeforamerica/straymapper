import os
import csv
from django.core.files.storage import default_storage
from django.core.files.images import ImageFile

from animals.models import Animal


def run():
    script_path = os.path.dirname(__file__)
    csv_file = open("%s/../fixtures/dataset_072012.csv" % script_path)
    contents = csv.reader(csv_file, dialect='excel', delimiter=',')
    header = contents.next()

    for row in contents:
        animal_id = row[3]
        s = '/home/michelle/work/CfA/Images/' + animal_id + '.jpg'

        try:
            with open(s, 'rb') as photo:
                if Animal.objects.filter(animal_id=animal_id):
                    a = Animal.objects.filter(animal_id=animal_id)[0]
                    imagephoto = ImageFile(photo)
                    a.photo.save(s, imagephoto, save=True)
                    print "appended photo to animal %s" % animal_id
                else:
                    print "have photo but missing record for %s" % animal_id

        except IOError:
            print "missing photo for " + animal_id
