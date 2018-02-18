from django.contrib import admin

from .models import Broker, Investor, TransactionType, Transaction, FundsTransfer, Fee

admin.site.register(Broker)
admin.site.register(Investor)
admin.site.register(TransactionType)
admin.site.register(Transaction)
admin.site.register(FundsTransfer)
admin.site.register(Fee)
