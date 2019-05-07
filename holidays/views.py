from django.views.generic.edit import CreateView
from .models import *
from .forms import *
from django.urls import reverse
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _


class CreateVacations(CreateView):
    model = Vacation
    form_class = VacationsForm

    def get_success_url(self):
        return reverse('staff:calendar', args=[self.object.start.year, self.object.start.month])

    def get_initial(self):
        initial = super().get_initial()
        initial.update({'user' : self.request.user})
        return initial

    def form_valid(self, form):
        response = super(CreateVacations, self).form_valid(form)
        messages.info(self.request, _('Your vacations request has been sent'))
        return response