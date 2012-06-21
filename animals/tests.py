from datetime import datetime

from django.core.urlresolvers import reverse
from django.test import TestCase

from animals.models import Animal

class AnimalsViewsTestCase(TestCase):
    fixtures = ['animals_testdata.json']

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
        resp = self.client.get(reverse('animals_index'))
        self.assertContains(resp, "map.addMarker", count=100, status_code=200)
