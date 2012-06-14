from django.contrib.gis.db import models

class Animal(models.Model):
    intake_date = models.DateField('Intake Date')
    location = models.CharField('Location', max_length=255)
    intake_condition = models.CharField('Intake Condition', max_length=255)
    animal_type = models.CharField('Animal Type', max_length=255)
    GENDER_CHOICES = (
        (u'M', u'Male'),
        (u'F', u'Female'),
        (u'S', u'Spayed'),
        (u'N', u'Neutered'),
    )
    sex = models.CharField('Sex', max_length=2, choices=GENDER_CHOICES)
    age = models.IntegerField('Age in Days')
    color = models.CharField('Color', max_length=255)
    breed = models.CharField('Breed', max_length=255)
    intake_total = models.IntegerField('Intake Total')
    animal_id = models.CharField('Animal ID', max_length=255,
        primary_key='True')
    geometry = models.PointField(srid=4326)

    objects = models.GeoManager()

    def __unicode__(self):
        return self.animal_id
