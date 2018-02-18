from decimal import Decimal

from django.views.generic.edit import CreateView

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from bonds.models import Bond
from .models import FundsTransfer, Transaction, Investor, Broker, Fee
from .forms import FundsTransferForm, TransactionForm, FeeForm

def index(request):
    bonds = Bond.objects.all()
    brokers = Broker.objects.all()
    return render(request, 'transactions/index.html', {'bonds': bonds, 'brokers': brokers})

class FundsTransferCreate(CreateView):
    model = FundsTransfer
    # fields = ['fromBroker', 'toBroker', 'amount']
    form_class = FundsTransferForm
    
    def form_valid(self, form):
        investor = Investor.objects.get(user=self.request.user)
        amt = Decimal(self.request.POST['amount'])

        # Unnecessary repetition of fields, see TransactionCreate below
        fromBrkId = self.request.POST['fromBroker']
        toBrkId = self.request.POST['toBroker']

        if fromBrkId != toBrkId:
            fromBrk = Broker.objects.get(pk=fromBrkId)
            toBrk = Broker.objects.get(pk=toBrkId)
            
            fromBrk.balance -= amt
            fromBrk.save()

            toBrk.balance += amt
            toBrk.save()
        
            ft = FundsTransfer(owner=investor,
                               fromBroker=fromBrk,
                               toBroker=toBrk,
                               amount=amt)
            ft.save()

        return HttpResponseRedirect(reverse("transactions:fundstransfer_transfer"))

class FeeCreate(CreateView):
    model = Fee
    form_class = FeeForm

    def form_valid(self, form):
        investor = Investor.objects.get(user=self.request.user)

        fee = form.save(commit=False)
        fee.owner = investor
        feeAmount = fee.amount
        fee.save()

        fee.broker.balance -= feeAmount
        fee.broker.save()

        return HttpResponseRedirect(reverse('transactions:fee_add'))

class TransactionCreate(CreateView):
    model = Transaction
    form_class = TransactionForm
    
    def form_valid(self, form):
        investor = Investor.objects.get(user=self.request.user)

        # _POST = self.request.POST
        # transactionTypeId = _POST['transactionType']
        # transactionDate = _POST['transactionDate']
        # brokerId = _POST['broker']
        # bondId = _POST['bond']
        # quantity = _POST['quantity']
        # totalPrice = _POST['totalPrice']
        # advertisedReturn = _POST['advertisedReturn']
        # notes = _POST['notes']

        # tr = Transaction(owner=investor, transactionType=
        
        # http://stackoverflow.com/questions/9900923/django-create-object-from-constructor-or-model-form

        tr = form.save(commit=False)
        tr.owner = investor
        totalPrice = tr.totalPrice
        tr.save()

        # Alter Broker's balance
        tr.broker.balance += tr.transactionType.factor * totalPrice
        tr.broker.save()
        
        
        return HttpResponseRedirect(reverse("transactions:transaction_add"))
