from django.views.generic.edit import CreateView
from django.contrib import messages
from .models import *
from .forms import *
from .utils import user_leave_summary
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect



class RequestLeave(LoginRequiredMixin, CreateView):
    model = Leave
    form_class = LeaveForm

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.staffprofile.department:
            messages.warning(request, "You need to be part of a deparment")
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['leave_summary'] = user_leave_summary(self.request.user)
        return context

    def get_success_url(self):
        return reverse('staff:calendar', args=[self.object.start.year, self.object.start.month])

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.info(self.request, _('Your leave request has been sent'))
        return response