from datetime import datetime

from django.core.urlresolvers import reverse
from django.test import TestCase

from animals.models import Animal


class AnimalsViewsTestCase(TestCase):
    fixtures = ['animals_testdata.json']

    def test_index(self):
        """
        Checks for 200 status and that expected variables in context
        and that some animals are displayed by default.
        """
        resp = self.client.get(reverse('animals_index'))
        self.assertTrue('form' in resp.context)
        self.assertTrue('alist' in resp.context)
        self.assertTrue('results_count' in resp.context)
        self.assertNotContains(resp, '<div>0 animals displayed</div>',
                               status_code=200)

    def test_type_search(self):
        resp = self.client.post(reverse('animals_index'), {
            'animal_type': 'CAT', 'intake_date_start': '2012-08-01'})
        self.assertContains(resp, "8/24/2012")
        self.assertContains(resp, "black domestic sh", status_code=200)

    def test_date_search(self):
        resp = self.client.post(reverse('animals_index'), {
            'intake_date_start': '2012-09-07',
            'intake_date_end': '2012-09-07'})
        self.assertContains(resp, "9/7/2012")
        self.assertContains(resp, "smokey")
        self.assertContains(resp, "tan pug mix", status_code=200)

    def test_paginated_type_search(self):
        self.client.post(reverse('animals_index'), {'animal_type': 'CAT',
                         'intake_date_start': '2012-08-01'})
        resp = self.client.get('%s?page=2' % reverse('animals_index'))
        self.assertContains(resp, "8/27/2012", count=1)
        self.assertContains(resp, "black domestic sh mix", status_code=200)

    def test_sex_search(self):
        resp = self.client.post(reverse('animals_index'), {'sex': 'M',
                                'intake_date_start': '2012-08-01'})
        self.assertContains(resp, "8/24/2012")
        self.assertContains(resp, "geek")
        self.assertContains(resp, "black tan chihuahua sh mix",
                            status_code=200)

    def test_condition_search(self):
        resp = self.client.post(reverse('animals_index'), {
            'intake_condition': 'INJURED', 'intake_date_start': '2012-08-01'})
        self.assertContains(resp, "8/26/2012")
        self.assertContains(resp, "chuck")
        self.assertContains(resp, "brown white chihuahua sh mix",
                            status_code=200)

    def test_markers_displayed(self):
        resp = self.client.post(reverse('animals_index'), {
            'intake_date_start': '2012-09-07',
            'intake_date_end': '2012-09-07'})
        self.assertContains(resp, "map.addMarker", count=18, status_code=200)
