from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings
from datetime import date, timedelta
from .models import *
from staff.models import Department
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


class VacationsTestCase(TestCase):

    fixtures = ['staff-testing-data.json', 'vacations-testing-data.json']

    def setUp(self):
        self.client = Client()
        self.department = Department.objects.create(name='department-test-example', vacations=20, personal_days=2)
        self.worker = get_user_model().objects.create(username='worker', email='worker@example.com')
        self.manager = get_user_model().objects.create(username='manager', email='manager@example.com')

    def test_vacations_admin(self):
        response = self.client.post(settings.LOGIN_URL, {'username': settings.DEFAULT_ADMIN_USERNAME, 'password': settings.DEFAULT_ADMIN_PASSWORD})
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('admin:holidays_vacation_changelist'))
        self.assertEqual(response.status_code, 200)

    def test_vacation_model(self):
        h = Vacation.objects.create(user=self.worker, start=date.today(), end=date.today() + timedelta(days=1))
        
        with self.assertRaisesMessage(ValidationError, 'worker must be in a department first'):
            h.clean()
        
        self.worker.staffprofile.department = self.department
        self.worker.staffprofile.save()

        h.save()
        
        with self.assertRaisesMessage(ValidationError, '%s is not a manager of %s department' % (self.manager, self.worker.staffprofile.department)):
            h.approved_by = self.manager
            h.clean()

        self.department.managers.add(self.manager)
       
