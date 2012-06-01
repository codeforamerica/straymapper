from django.db import models


class Animal(models.Model): 
    # intake_date looks like 5/28/2012 12:00:00 AM, should it be a DateField?	
    intake_date = models.DateField('Intake Date')
    #location is an address such as '9411 BARNESDALLE AUSTIN TX'	
    location = models.CharField('Location', max_length=255)
    #intake_condition descibes the state of the animal at intake, should there be choices? e.g. 'INJURED', 'SICK', 'AGED'  
    intake_condition = models.CharField('Intake Condition', max_length=255) 
    #animal_type is usually 'CAT' or 'DOG' but not always? 
    # Should this be a choice? 
    animal_type = models.CharField('Animal Type', max_length=255) 
    # sex is one of 'S', 'M', 'N', or 'F' 
    GENDER_CHOICES = (
        (u'M', u'Male'),
        (u'F', u'Female'),
        (u'S', u'Spayed'), 
        (u'N', u'Neutered'),
    )
    sex = models.CharField('Sex', max_length=2, choices=GENDER_CHOICES)
    #age looks like '13.05 yr'
    age = models.IntegerField('Age in Days')
    #color looks like 'TORBIE' 
    color = models.CharField('Color', max_length=255)
    #breed looks like 'DOMESTIC SH'
    breed = models.CharField('Breed', max_length=255) 
    #intake total is an int 
    intake_total = models.IntegerField('Intake Total') 
    #Animal ID looks like A163112, we want this as our primary key 
    animal_id = models.CharField('Animal ID', max_length=255, primary_key='True')

    def __unicode__(self): 
        return self.animal_id
    



