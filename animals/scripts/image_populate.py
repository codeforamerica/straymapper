import os 
import csv 

from animals.models import Animal 

def run(): 
    csv_file = open("%s/../fixtures/DataSet1.csv" % os.path.dirname(__file__)) 
    contents = csv.reader(csv_file, dialect='excel', delimiter=',') 
    header = contents.next() 
    
    for row in contents: 
        animal_id = row[3] 
        s = '~/michelle/work/CfA/Images/' + animal_id + '.jpg' 

        if open(s, 'rb').exists(): 
            f = open(s, 'rb')
            a = Animal.objects.filter(animal_id=animal_id)
            a.photo = f 

            print "appended photo to animal %s" % animal_id 

        else: 
            pass 
