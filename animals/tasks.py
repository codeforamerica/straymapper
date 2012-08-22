from celery import task

@task()
def populate(animal_id):
    return 'processing %s' % animal_id
