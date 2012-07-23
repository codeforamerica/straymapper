import os 
import csv 

from animals.models import Animal 

def run(): 
    csv_file = open("%s/../fixtures/dataset_072012.csv" % os.path.dirname(__file__)) 
    contents = csv.reader(csv_file, dialect='excel', delimiter=',') 
    header = contents.next() 
    
    for row in contents: 
        animal_id = row[3] 
        s = '~/michelle/work/CfA/Images/' + animal_id + '.jpg' 

        try: 
            with open(s, 'rb') as f: 
                a = Animal.objects.filter(animal_id=animal_id)
                a.photo = f 
                print "appended photo to animal %s" %animal_id 
        
        except IOError as e: 
            print "missing " + animal_id
