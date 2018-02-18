from math import exp, log

# General formulas

def fmtFV(fv):
    return "{:,.2f}".format(fv)
    
def simpleComp(periods, pr=10, pv=100):
    r = pr / 100
    return fmtFV(pv * (1+r)**periods)

def contComp(periods, pr=10, pv=100):
    """FV = PV * e^(r*t)"""
    r = pr / 100    
    return fmtFV(pv * exp(r * periods))

def computeAnn(fv, pv, daysDiff):
    r = log(fv / pv) / (daysDiff / 365.25)
    return exp(r) - 1
