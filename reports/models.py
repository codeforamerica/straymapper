from django.contrib.gis.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, Adjust


class Report(models.Model):
    TYPE_CHOICES = (
        (u'PUPPY', u'Puppy'),
        (u'KITTEN', u'Kitten'),
        (u'DOG', u'Dog'),
        (u'CAT', u'Cat'),
    )

    GENDER_CHOICES = (
        (u'M', u'Male'),
        (u'F', u'Female'),
        (u'U', u'Unknown'),
    )

    missing_since = models.DateField()
    location = models.CharField(max_length=255)
    animal_type = models.CharField(max_length=255, choices=TYPE_CHOICES)
    sex = models.CharField(max_length=2, choices=GENDER_CHOICES)
    name = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='straymapper/report-photos',
                              blank=True, null=True)
    thumbnail = ImageSpecField([Adjust(contrast=1.2, sharpness=1.1),
                               ResizeToFill(120, 90)], image_field='photo',
                               format="JPEG", options={'quality': 90})

    geometry = models.PointField(srid=4326)

    objects = models.GeoManager()

    def __unicode__(self):
        return self.name
