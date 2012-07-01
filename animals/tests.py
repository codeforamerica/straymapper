from datetime import datetime

from django.core.urlresolvers import reverse
from django.test import TestCase

from animals.models import Animal


class AnimalsViewsTestCase(TestCase):
    fixtures = ['animals_testdata.json']

    def test_index(self):
        """
	Checks for 200 status and that expected variables in context and that some 
	animals are displayed by default.
        """
        resp = self.client.get(reverse('animals_index'))
        self.assertTrue('form' in resp.context)
        self.assertTrue('alist' in resp.context)
        self.assertTrue('results_count' in resp.context)
        self.assertNotContains(resp, '0 animals displayed', status_code=200)

    def test_type_search(self):
        resp = self.client.post(reverse('animals_index'),
            {'animal_type': 'CAT'})
        self.assertContains(resp, "5/31/2012")
        self.assertContains(resp, "cypress")
        self.assertContains(resp, "brn tabby domestic sh", status_code=200)

    def test_sex_search(self):
        resp = self.client.post(reverse('animals_index'), {'sex': 'M'})
        self.assertContains(resp, "5/30/2012")
        self.assertContains(resp, "beagle")
        self.assertContains(resp, "tricolor beagle", status_code=200)

    def test_date_search(self):
        resp = self.client.post(reverse('animals_index'),
            {'intake_date': '2012-06-04'})
        self.assertContains(resp, "6/4/2012")
        self.assertContains(resp, "chalupa")
        self.assertContains(resp, "white rat terrier", status_code=200)

    def test_condition_search(self):
        resp = self.client.post(reverse('animals_index'),
            {'intake_condition': 'INJURED'})
        self.assertContains(resp, "5/30/2012")
        self.assertContains(resp, "bo jangles")
        self.assertContains(resp, "white catahoula", status_code=200)

    def test_markers_displayed(self):
        resp = self.client.post(reverse('animals_index'),
            {'intake_date': '2012-06-04'})
        self.assertContains(resp, "map.addMarker", count=4, status_code=200)
