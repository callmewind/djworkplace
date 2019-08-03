from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings

# Create your tests here.

class CalendarTestCase(TestCase):

    fixtures = ['staff-testing-data.json', 'leave-testing-data.json']

    def setUp(self):
        pass

    def test_calendar_view(self):
        c = Client()
        response = c.post(settings.LOGIN_URL, {'username': settings.DEFAULT_ADMIN_USERNAME, 'password': settings.DEFAULT_ADMIN_PASSWORD})
        self.assertEqual(response.status_code, 302)
        response = c.get(reverse('staff:calendar'))
        self.assertEqual(response.status_code, 200)

    def test_staff_admin(self):
        c = Client()
        response = c.post(settings.LOGIN_URL, {'username': settings.DEFAULT_ADMIN_USERNAME, 'password': settings.DEFAULT_ADMIN_PASSWORD})
        self.assertEqual(response.status_code, 302)
        response = c.get(reverse('admin:auth_user_changelist'))
        self.assertEqual(response.status_code, 200)