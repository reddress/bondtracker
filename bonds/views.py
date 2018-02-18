from django.views.generic.edit import CreateView

from django.shortcuts import render

from .models import Bond
from .forms import BondForm

class BondCreate(CreateView):
    model = Bond
    form_class = BondForm

