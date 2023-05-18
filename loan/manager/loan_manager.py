class LoanManager:
    def update_loan_status(self):
        status = None
        loans = Loan.objects.filter(is_active=True, is_deleted=False)
        print("-----loans")
        print(loans)
        if loans:
            update_loans = loans.update(status==1)
            return update_loans
        else:
            pass