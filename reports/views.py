from collections import namedtuple, defaultdict

from django.shortcuts import render, get_object_or_404, redirect
from django.utils.http import is_safe_url
from django.urls import reverse

from transactions.models import Broker, Transaction, Investor
from bonds.models import BondType, Bond
from .calculator import transactions_total, aggregateTransactions, BrokerBonds, BondTypeBonds, addAnnualizedRates
from .util import parseDate, parseFromDate, parseToDate, displayDate
from .util import DEFAULT_FROM_DATE, DEFAULT_TO_DATE

def index(request):
    return render(request, 'reports/index.html')

# Produce lists of entities
def brokers(request):
    investor = Investor.objects.get(user=request.user)
    brokers = Broker.objects.filter(client=investor)
    return render(request, 'reports/brokers.html', {'brokers': brokers})

def bondtypes(request):
    bondtypes = BondType.objects.all()
    return render(request, 'reports/bondtypes.html', {'bondtypes': bondtypes})

def bonds(request):
    bonds = Bond.objects.all()
    return render(request, 'reports/bonds.html', {'bonds': bonds})

# Retrieve transactions
CommonTransactionData = namedtuple("CommonTransactionData",
                                   ["investor", "from_date", "to_date"])

def get_common_data(request):
    return CommonTransactionData(Investor.objects.get(user=request.user),
                                 parseFromDate(request),
                                 parseToDate(request))

def byBroker(request, broker_id):
    broker = get_object_or_404(Broker, pk=broker_id)

    common = get_common_data(request)
                                   
    transactions = Transaction.objects.filter(
        broker=broker,
        owner=common.investor,
        transactionDate__gte=common.from_date,
        transactionDate__lte=common.to_date)
    
    total = transactions_total(transactions)

    addAnnualizedRates(transactions)

    return render(request, 'reports/byBroker.html',
                  {'broker': broker,
                   'transactions': transactions,
                   'total': total})
    
def byBondType(request, bondtype_id):
    bondtype = get_object_or_404(BondType, pk=bondtype_id)
    matching_bonds = Bond.objects.filter(bondtype=bondtype)

    common = get_common_data(request)
    
    transactions = Transaction.objects.filter(
        owner=common.investor,
        bond__in=matching_bonds,
        transactionDate__gte=common.from_date,
        transactionDate__lte=common.to_date)
    
    total = transactions_total(transactions)

    addAnnualizedRates(transactions)

    return render(request, 'reports/byBondType.html',
                  {'bondtype': bondtype,
                   'transactions': transactions,
                   'total': total})

def byBond(request, bond_id):
    bond = get_object_or_404(Bond, pk=bond_id)

    common = get_common_data(request)
    
    transactions = Transaction.objects.filter(
        owner=common.investor,
        bond=bond,
        transactionDate__gte=common.from_date,
        transactionDate__lte=common.to_date)
    
    total = transactions_total(transactions)

    addAnnualizedRates(transactions)

    return render(request, 'reports/byBond.html',
                  {'bond': bond,
                   'transactions': transactions,
                   'total': total})

def allTransactions(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login/?next=/')
    
    common = get_common_data(request)

    transactions = Transaction.objects.filter(
        owner=common.investor,
        transactionDate__gte=common.from_date,
        transactionDate__lte=common.to_date)

    total = transactions_total(transactions)

    addAnnualizedRates(transactions)

    return render(request, 'reports/allTransactions.html',
                  {'transactions': transactions,
                   'total': total})
    
def changeDates(request):
    if request.method == "POST":
        fromDate = parseDate(request.POST['from'], DEFAULT_FROM_DATE)
        toDate = parseDate(request.POST['to'], DEFAULT_TO_DATE)

        # save parsed dates to session data
        request.session['fromDate'] = displayDate(fromDate)
        request.session['toDate'] = displayDate(toDate)
        
        if is_safe_url(request.POST['prevUrl']):
            return redirect(request.POST['prevUrl'])
    return redirect(reverse('reports:index'))

def resetDates(request):
    request.session['fromDate'] = displayDate(DEFAULT_FROM_DATE)
    request.session['toDate'] = displayDate(DEFAULT_TO_DATE)
    if is_safe_url(request.GET['prevUrl']):
        return redirect(request.GET['prevUrl'])
    return redirect(reverse('reports:index'))

# aggregate reports

def aggregateAll(request):
    common = get_common_data(request)
    
    transactions = Transaction.objects.filter(
        owner=common.investor,
        transactionDate__gte=common.from_date,
        transactionDate__lte=common.to_date)

    aggregates = aggregateTransactions(transactions)

    total = transactions_total(transactions)

    return render(request, 'reports/aggregateAll.html',
                  {'aggregates': aggregates, 'total': total})

def aggregateByBroker(request):
    common = get_common_data(request)

    brokers = Broker.objects.filter(client=common.investor)

    # want to return
    # brokerAggregate = [{'name': 'Itau', 'bonds': [{'name': 'LTN' ...

    brokersDict = defaultdict(BrokerBonds)

    for broker in brokers:
        transactions = Transaction.objects.filter(
            broker=broker,
            owner=common.investor,
            transactionDate__gte=common.from_date,
            transactionDate__lte=common.to_date)

        brokersDict[broker.name].name = broker.name
        brokersDict[broker.name].total = transactions_total(transactions)
        brokersDict[broker.name].bonds = aggregateTransactions(transactions)

    sortedBrokerNames = sorted(brokersDict)
    
    result = []
    
    for brokerName in sortedBrokerNames:
        result.append({'name': brokerName,
                       'total': brokersDict[brokerName].total,
                       'aggregates': brokersDict[brokerName].bonds})

    return render(request, 'reports/aggregateByBroker.html',
                  {'brokers': result})

def aggregateByBondType(request):
    common = get_common_data(request)

    bondtypes = BondType.objects.all()

    bondtypesDict = defaultdict(BondTypeBonds)

    for bondtype in bondtypes:
        transactions = Transaction.objects.filter(
            bond__bondtype=bondtype,
            owner=common.investor,
            transactionDate__gte=common.from_date,
            transactionDate__lte=common.to_date)

        bondtypesDict[bondtype.code].name = str(bondtype)
        bondtypesDict[bondtype.code].total = transactions_total(transactions)
        bondtypesDict[bondtype.code].bonds = aggregateTransactions(transactions)

    sortedBondtypeNames = sorted(bondtypesDict)
    
    result = []
    
    for bondtypeName in sortedBondtypeNames:
        result.append({'name': bondtypesDict[bondtypeName].name,
                       'total': bondtypesDict[bondtypeName].total,
                       'aggregates': bondtypesDict[bondtypeName].bonds})

    return render(request, 'reports/aggregateByBondType.html',
                  {'bondtypes': result})
