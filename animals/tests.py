from django.core.urlresolvers import reverse
from django.test import TestCase


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

