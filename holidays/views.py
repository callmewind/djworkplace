from django.views.generic.edit import CreateView
from .models import *
from .forms import *
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin


class CreateVacations(LoginRequiredMixin, CreateView):
    model = Vacation
    form_class = VacationsForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = timezone.now().year
        approved = 0
        pending_approval = 0
        #for v in Vacation.objects.filter(user=self.request.user).filter(Q(start__year=year)|Q(end__year=year)):
            
        return context

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