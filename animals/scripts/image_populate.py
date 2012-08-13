import csv
import os
import urllib

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
        print animal_id
        filename = animal_id + '.jpg'
        s = 'https://citypetz.s3.amazonaws.com/images/' + filename
        print s
        temp_photo = urllib.urlretrieve(s, '/tmp/%s' % filename)

        try:
            photo = open(temp_photo[0], 'rb')
            print photo
            if Animal.objects.filter(animal_id=animal_id).exists():
                a = Animal.objects.get(animal_id=animal_id)
                imagephoto = ImageFile(photo)
                a.photo.save(filename, imagephoto, save=True)
                print "appended photo to animal"
                thumb = a.thumbnail
                thumb_url = a.thumbnail.url
            else:
                print "have photo but missing record for %s" % animal_id
        except IOError:
            print "missing photo for " + animal_id
