from datetime import datetime

from django.core.urlresolvers import reverse
from django.test import TestCase

from animals.models import Animal

class AnimalsViewsTestCase(TestCase):
    def test_index(self):
        resp = self.client.get(reverse('animals_index'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('form' in resp.context)
        self.assertTrue('alist' in resp.context)
        self.assertTrue('results_count' in resp.context)

    def test_cat_search(self):
        resp = self.client.post(reverse('animals_index'), {'animal_type': 'CAT'})
        self.assertEqual(resp.status_code, 200)

    def test_markers_displayed(self):
        Animal.objects.create(
            intake_date=datetime.today(),
            location="9411 BARNESDALLE AUSTIN TX",
            intake_condition='NORMAL',
            animal_type='CAT',
            sex='M',
            age=4763,
            name='Pepper',
            description='gray schnauzer min',
            intake_total=2,
            animal_id='A163112',
            geometry='POINT (-97.7932349999999957 30.1910789999999984)'
        )
        resp = self.client.get(reverse('animals_index'))
        self.assertContains(resp, "map.addMarker", status_code=200)
