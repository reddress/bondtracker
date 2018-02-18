from django.conf.urls import url

from django.contrib.auth.decorators import login_required

from . import views

app_name = 'transactions'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'fundstransfer/transfer/$', login_required(views.FundsTransferCreate.as_view()), name='fundstransfer_transfer'),
    url(r'transaction/add/$', login_required(views.TransactionCreate.as_view()), name='transaction_add'),
    url(r'fee/add/$', login_required(views.FeeCreate.as_view()), name='fee_add'),
]
