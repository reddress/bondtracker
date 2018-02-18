from django.db import models

class BondType(models.Model):
    """A type of bond, independent of maturity"""
    name = models.CharField(max_length=80)  # NTN-B Principal
    code = models.CharField(max_length=20)
    prefixed = models.BooleanField()
    hasCoupon = models.BooleanField()

    def __str__(self):
        return "{} ({})".format(self.code, self.name)

    class Meta:
        ordering = ['code']
    
class Bond(models.Model):
    bondtype = models.ForeignKey(BondType, on_delete=models.SET_NULL, null=True)
    maturity = models.DateField()
    latestPrice = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    latestPriceDate = models.DateField(blank=True, null=True)

    def __str__(self):
        price = ""
        priceDate = ""
        if self.latestPrice is not None:
            price = " <R$ " + str(self.latestPrice) + ">"
            priceDate = self.latestPriceDate.strftime("%d/%m/%y")
            
        return str(self.bondtype.code) + " " + str(self.maturity.strftime("%Y")) + price + " " + priceDate

    class Meta:
        ordering = ['bondtype', 'maturity']
