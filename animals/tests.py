from django.test import TestCase


class AnimalsViewsTestCase(TestCase):
    def test_index(self):
        resp = self.client.get('/animals/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('form' in resp.context)
        self.assertTrue('alist' in resp.context)
        self.assertTrue('results_count' in resp.context)

