from django.conf.urls import url
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required

from . import views

app_name = 'bonds'

urlpatterns = [
    url(r'bond/add/$', login_required(views.BondCreate.as_view(success_url=reverse_lazy('bonds:bond_add'))), name='bond_add'),
]
