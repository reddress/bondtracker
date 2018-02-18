from django.forms import ModelForm
from django.contrib.admin import widgets

from .models import Transaction, FundsTransfer, Fee

class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ['transactionType', 'transactionDate', 'broker',
                  'bond', 'quantity', 'totalPrice', 'advertisedReturn',
                  'notes']

    def __init__(self, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.fields['transactionDate'].widget = widgets.AdminDateWidget()

class FundsTransferForm(ModelForm):
    class Meta:
        model = FundsTransfer
        fields = ['fromBroker', 'toBroker', 'amount']

class FeeForm(ModelForm):
    class Meta:
        model = Fee
        fields = ['broker', 'feeDate', 'amount', 'notes']

    def __init__(self, *args, **kwargs):
        super(FeeForm, self).__init__(*args, **kwargs)
        self.fields['feeDate'].widget = widgets.AdminDateWidget()
