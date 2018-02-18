from django.contrib import admin

from .models import BondType, Bond

admin.site.register(BondType)
admin.site.register(Bond)
