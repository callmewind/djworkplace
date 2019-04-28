from django.views.generic.edit import CreateView
from .models import *
from .forms import *


class CreateHoliday(CreateView):
    model = Holiday
    form_class = HolidayForm