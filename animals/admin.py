from django.contrib.gis import admin

from animals.models import Animal


class AnimalAdmin(admin.GeoModelAdmin):
    list_display = ('animal_id', 'intake_date', 'animal_type', 'sex')
    search_fields = ('animal_id', 'name')
    ordering = ('-intake_date',)

admin.site.register(Animal, AnimalAdmin)
