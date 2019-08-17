from django.views.generic.edit import CreateView
from django.contrib import messages
from .models import *
from .forms import *
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone
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
        year = timezone.now().year
        context['leaves'] = {}
        user_leave = UserLeave.objects.get(pk=self.request.user.pk)
        for leave_limit in self.request.user.staffprofile.department.leave_limits.all().select_related('type'):
            type_data = {
                'approved'  : user_leave.current_year_approved_leaves(leave_limit.type),
                'pending'   : user_leave.current_year_pending_leaves(leave_limit.type),
                'total'     : leave_limit.days
            }
            type_data['available'] = max(type_data['total'] - type_data['approved'] - type_data['pending'], 0)
            context['leaves'][leave_limit.type] = type_data   
        return context

    def get_success_url(self):
        return reverse('staff:calendar', args=[self.object.start.year, self.object.start.month])

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.info(self.request, _('Your leave request has been sent'))
        return response