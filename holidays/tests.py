from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings


class HolidaysTestCase(TestCase):

    fixtures = ['testing-data.json']

    def setUp(self):
        pass

    def test_holiday_admin(self):
        c = Client()
        response = c.post(settings.LOGIN_URL, {'username': settings.DEFAULT_ADMIN_USERNAME, 'password': settings.DEFAULT_ADMIN_PASSWORD})
        self.assertEqual(response.status_code, 302)
        response = c.get(reverse('admin:holidays_holiday_changelist'))
        self.assertEqual(response.status_code, 200)