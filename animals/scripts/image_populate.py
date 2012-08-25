import csv
import os
import urllib

import requests

from django.core.files.storage import default_storage
from django.core.files.images import ImageFile

from animals.models import Animal


def run():
    for a in Animal.objects.filter(photo=u''):
        print a.animal_id
        filename = a.animal_id + '.jpg'
        s = 'https://citypetz.s3.amazonaws.com/images/' + filename
        print s

        r = requests.head(s)
        if r.status_code == 200:
            temp_photo = urllib.urlretrieve(s, '/tmp/%s' % filename)

            try:
                if temp_photo:
                    photo = open(temp_photo[0], 'rb')
                    print photo
                    imagephoto = ImageFile(photo)
                    a.photo.save(filename, imagephoto, save=True)
                    print "appended photo to animal"
                    thumb = a.thumbnail
                    thumb_url = a.thumbnail.url
                else:
                    print "have record but missing photo for %s" % a.animal_id
            except IOError:
                print "missing photo for " + a.animal_id
        else:
            print "missing photo for " + a.animal_id
