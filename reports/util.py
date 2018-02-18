from datetime import date, datetime

DEFAULT_FROM_DATE = date(2001, 1, 1)
DEFAULT_TO_DATE = date(2068, 1, 1)

def parseDate(s, defaultDate=DEFAULT_FROM_DATE):
    """Parse a string s in the formats 15/01/16 or 15/01/2016"""
    try:
        # 2-digit year
        parsedDate = datetime.strptime(s, "%d/%m/%y")
    except ValueError:
        try:
            # 4-digit year
            parsedDate = datetime.strptime(s, "%d/%m/%Y")
        except ValueError:  # some other invalid format
            parsedDate = defaultDate
    except KeyError:
        parsedDate = defaultDate
    return parsedDate
    
def parseFromDate(request):
    try:
        parsedDate = parseDate(request.session['fromDate'], DEFAULT_FROM_DATE)
    except KeyError:
        parsedDate = DEFAULT_FROM_DATE
    request.session['fromDate'] = displayDate(parsedDate)
    return parsedDate

def parseToDate(request):
    try:
        parsedDate = parseDate(request.session['toDate'], DEFAULT_TO_DATE)
    except KeyError:
        parsedDate = DEFAULT_TO_DATE
    request.session['toDate'] = displayDate(parsedDate)
    return parsedDate

def displayDate(d):
    return d.strftime("%d/%m/%y")
