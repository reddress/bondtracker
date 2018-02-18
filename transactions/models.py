from decimal import Decimal

from django.db import models
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags.humanize import intcomma

from bonds.models import Bond

class Investor(models.Model):
    """A person who buys and sells bonds."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currencyCode = models.CharField(max_length=10)  # single currency per investor (user)

    def __str__(self):
        return self.user.username

class Broker(models.Model):
    client = models.ForeignKey(Investor, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=80)
    manager = models.CharField(max_length=80, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name + " (" + intcomma(str(self.balance)) + ")"

    class Meta:
        ordering = ['name']
            
class TransactionType(models.Model):
    factor = models.IntegerField(default=1)  # Sale = 1, Purchase = -1

    def __str__(self):
        if self.factor == 1:
            transactionType = "Sell"
        elif self.factor == -1:
            transactionType = "Buy"
        else:
            transactionType = "Custom type: factor=" + str(factor)
        return transactionType

    class Meta:
        ordering = ['factor']

class Transaction(models.Model):
    owner = models.ForeignKey(Investor, on_delete=models.SET_NULL, null=True)
    transactionType = models.ForeignKey(TransactionType, on_delete=models.SET_NULL, null=True)
    transactionDate = models.DateField()
    broker = models.ForeignKey(Broker, on_delete=models.SET_NULL, null=True)
    bond = models.ForeignKey(Bond, on_delete=models.SET_NULL, null=True)
    quantity = models.DecimalField(max_digits=6, decimal_places=2)
    totalPrice = models.DecimalField(max_digits=10, decimal_places=2)
    
    # the yearly percentage return quoted on the purchase page
    advertisedReturn = models.CharField(max_length=20, blank=True)

    # stuff like 'Protocolo number'
    notes = models.CharField(max_length=80, blank=True)

    def __str__(self):
        return "{} {} x{} {} {} {}".format(
            self.transactionDate.strftime("%d/%m/%y"),
            self.bond,
            str(self.quantity),
            self.broker.name,
            self.owner.currencyCode,
            str(self.totalPrice))
        
    class Meta:
        ordering = ['-transactionDate', 'broker', 'bond']
    
class FundsTransfer(models.Model):
    owner = models.ForeignKey(Investor, on_delete=models.SET_NULL, null=True)
    fromBroker = models.ForeignKey(Broker, on_delete=models.SET_NULL, null=True, related_name='transferFrom')
    toBroker = models.ForeignKey(Broker, on_delete=models.SET_NULL, null=True, related_name='transferTo')
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return "{} {} from {} to {}".format(self.owner.currencyCode, str(self.amount), self.fromBroker.name, self.toBroker.name)
        
class Fee(models.Model):
    owner = models.ForeignKey(Investor, on_delete=models.SET_NULL, null=True)
    broker = models.ForeignKey(Broker, on_delete=models.SET_NULL, null=True)
    feeDate = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.CharField(max_length=80, blank=True)

    def __str__(self):
        return "{} {} {}".format(self.broker.name, self.owner.currencyCode, str(self.amount))
