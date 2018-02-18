from django.forms import ModelForm
from django.contrib.admin import widgets

from .models import Bond

class BondForm(ModelForm):
    class Meta:
        model = Bond
        fields = ['bondtype', 'maturity']

    def __init__(self, *args, **kwargs):
        super(BondForm, self).__init__(*args, **kwargs)
        self.fields['maturity'].widget = widgets.AdminDateWidget()
        # self.fields['latestPriceDate'].widget = widgets.AdminDateWidget()
