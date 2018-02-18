# Format raw data to HTML

from transactions.models import Transaction

def wrap_in_td(s):
    return "<td>{}</td>".format(s)

def tabulate_transactions(trs):
    """Given a list of transactions trs, produce an HTML table"""
    result = "<table>\n"
    
    for tr in trs:
        columns = [str(tr.transactionType),
                   tr.transactionDate.strftime("%d/%m/%y"),
                   tr.broker.name,
                   str(tr.bond),
                   str(tr.quantity),
                   str(tr.totalPrice),
                   tr.advertisedReturn,
                   tr.notes]
        
        result += "<tr>"
        result += "\n".join(map(wrap_in_td, columns))
        result += "</tr>"

    return result
