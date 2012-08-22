from celery import task

@task()
def populate(message):
    return message + ' done'
