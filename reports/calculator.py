from decimal import Decimal
from collections import defaultdict
from datetime import date
from math import exp, log

from django.db.models import Sum

from transactions.models import Transaction

def transactions_total(trs):
    """Sum the total amount for the given transactions, trs"""
    total = Decimal('0.00')

    for tr in trs:
        total += tr.transactionType.factor * tr.totalPrice
    return -total  # make total the amount held, not spent

class BondTotal:
    def __init__(self):
        self.quantity = Decimal("0.00")
        self.totalPrice = Decimal("0.00")

    def __iter__(self):
        yield self.quantity
        yield self.totalPrice

    def __repr__(self):
        return "x{} {}".format(self.quantity, self.totalPrice)

class BrokerBonds:
    def __init__(self):
        self.bonds = []

    def __iter__(self):
        yield self.bonds

class BondTypeBonds:
    def __init__(self):
        self.bonds = []

    def __iter__(self):
        yield self.bonds

def aggregateTransactions(trs):
    """Collect total quantity and amount invested, grouped by bond"""
    bonds = defaultdict(BondTotal)
    for tr in trs:
        fullName = str(tr.bond)
        bonds[fullName].id = tr.bond.id
        bonds[fullName].name = str(tr.bond.bondtype.code)
        bonds[fullName].maturity = tr.bond.maturity.strftime("%d/%m/%y")
        bonds[fullName].maturityYMD = tr.bond.maturity.strftime("%Y-%m-%d")
        bonds[fullName].quantity -= tr.transactionType.factor * tr.quantity
        bonds[fullName].totalPrice -= tr.transactionType.factor * tr.totalPrice
        if tr.bond.latestPrice is not None:
            bonds[fullName].latestPrice = tr.bond.latestPrice
            bonds[fullName].latestPriceDate = tr.bond.latestPriceDate
        else:
            bonds[fullName].latestPrice = 0
            bonds[fullName].latestPriceDate = date.today()
    sortedBondNames = sorted(bonds)

    result = []
    
    for bondName in sortedBondNames:
        result.append({'name': bonds[bondName].name,
                       'id': bonds[bondName].id,
                       'maturity': bonds[bondName].maturity,
                       'maturityYMD': bonds[bondName].maturityYMD,
                       'quantity': bonds[bondName].quantity,
                       'totalPrice': bonds[bondName].totalPrice,
                       'latestPrice': "{:,.2f}".format(bonds[bondName].latestPrice),
                       'totalLatestPrice': "{:,.2f}".format(bonds[bondName].quantity * bonds[bondName].latestPrice),
                       'latestPriceDate': bonds[bondName].latestPriceDate,
                       'sortablePrice': str(bonds[bondName].totalPrice).zfill(11).replace(".", "")})

    return result

def computeAnnualizedRate(latestPrice, purchasePrice, qty, latestDate, purchaseDate):
    daysDiff = (latestDate - purchaseDate).days
    if daysDiff <= 0:
        return "N/A"
        
    fv = float(latestPrice)
    pv = float(purchasePrice) / float(qty)
    
    # dailyRate = (fv/pv) ** (1/daysDiff) - 1
    # return "{:.2f}%".format(100 * (((1 + dailyRate) ** 365.25) - 1))

    # derivation:
    # PV * exp(numPeriods * r) = FV
    # log(exp(numPeriods * r)) = log(FV / PV)
    # r = log(FV / PV) / numPeriods

    # to get yearly equivalent, take exp(r) and subtract 1
    compoundRate = log(fv / pv) / (daysDiff / 365.25)
    return "{:.2f}%".format(100 * (exp(compoundRate) - 1))

def addAnnualizedRates(trs):
    """Given a list of transactions, add an annualized rate property"""
    for tr in trs:
        if tr.bond.latestPrice is not None:
            if tr.transactionType.factor == -1: 
                tr.annualizedRate = computeAnnualizedRate(tr.bond.latestPrice, tr.totalPrice, tr.quantity, tr.bond.latestPriceDate, tr.transactionDate)
                if tr.annualizedRate == "N/A":
                    tr.sortAnnualizedRate = ""
                else:
                    tr.sortAnnualizedRate = str(tr.annualizedRate)[:-1].zfill(7)
                tr.latestPriceDate = tr.bond.latestPriceDate
                tr.marketPrice = "{:,.2f}".format(tr.bond.latestPrice * tr.quantity)
                tr.unitPrice = "{:,.2f}".format(tr.bond.latestPrice)
            else:
                tr.annualizedRate = "(sale)" 
            
