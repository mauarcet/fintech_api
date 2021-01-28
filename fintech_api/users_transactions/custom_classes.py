from django.db.models import Sum

class AccountSummary:
    def __init__(self, account, total_inflow, total_outflow, balance):
        self.account = account
        self.total_inflow = total_inflow
        self.total_outflow = total_outflow
        self.balance = balance

    @classmethod
    def fromTransactions(cls, transactions):
        accounts = []
        summary = []
        for t in transactions:
            if t.account not in accounts:
                accounts.append(t.account)
        for account in accounts:
            transactions_by_account = transactions.filter(account=account)
            inflow = transactions_by_account.filter(type='inflow').aggregate(Sum('amount'))
            outflow = transactions_by_account.filter(type='outflow').aggregate(Sum('amount'))
            if inflow['amount__sum'] is not None:
                total_inflow = inflow['amount__sum']
            else: 
                total_inflow = 0
            if outflow['amount__sum'] is not None:
                total_outflow = outflow['amount__sum']
            else:
                total_outflow = 0
            balance = total_inflow + total_outflow
            account_summary = cls(account, total_inflow, total_outflow, balance)
            summary.append(account_summary)
        return summary
    