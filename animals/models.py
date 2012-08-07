from django.contrib.gis.db import models
from imagekit.models import ImageSpecField 
from imagekit.processors import ResizeToFill, Adjust

class Animal(models.Model):
    intake_date = models.DateField('Intake Date')
    location = models.CharField('Location', max_length=255)
    intake_condition = models.CharField('Intake Condition', max_length=255)
    TYPE_CHOICES = (
        (u'PUPPY', u'Puppy'),
        (u'KITTEN', u'Kitten'),
        (u'DOG', u'Dog'),
        (u'CAT', u'Cat'),
    )
    animal_type = models.CharField('Animal Type', max_length=255,
        choices=TYPE_CHOICES)
    GENDER_CHOICES = (
        (u'M', u'Male'),
        (u'F', u'Female'),
        (u'U', u'Unknown'),
    )
    sex = models.CharField('Sex', max_length=2, choices=GENDER_CHOICES)
    spayed = models.BooleanField('Spayed or Neutered', default=False)
    age = models.IntegerField('Age in Days')
    name = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=255)
    intake_total = models.IntegerField('Intake Total')
    animal_id = models.CharField('Animal ID', max_length=255)
    photo = models.ImageField(upload_to='photo', blank=True, null=True)
 
    geometry = models.PointField(srid=4326)

    objects = models.GeoManager()

    def __unicode__(self):
        return self.animal_id
