from django.conf.urls import url

from . import views

app_name = 'reports'

urlpatterns = [
    # url(r'^$', views.index, name='index'),
    url(r'^$', views.allTransactions, name='index'),
    url(r'^brokers/$', views.brokers, name='brokers'),
    url(r'^bondtypes/$', views.bondtypes, name='bondtypes'),
    url(r'^bonds/$', views.bonds, name='bonds'),
    url(r'^by-broker/(?P<broker_id>[0-9]+)/$', views.byBroker, name='by-broker'),
    url(r'^by-bondtype/(?P<bondtype_id>[0-9]+)/$', views.byBondType, name='by-bond-type'),
    url(r'^by-bond/(?P<bond_id>[0-9]+)/$', views.byBond, name='by-bond'),
    url(r'^changeDates/$', views.changeDates, name="changeDates"),
    url(r'^resetDates/$', views.resetDates, name="resetDates"),
    url(r'^all-transactions/$', views.allTransactions, name="all-transactions"),
    url(r'^aggregate/all/$', views.aggregateAll, name="aggregateAll"),
    url(r'^aggregate/by-broker/$', views.aggregateByBroker, name="aggregateByBroker"),
    url(r'^aggregate/by-bondtype/$', views.aggregateByBondType, name="aggregateByBondType"),
]
