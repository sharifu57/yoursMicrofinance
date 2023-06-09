from loan.models import *
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
        
    def get_loan_details(self, loan_id):
        loan = Loan.objects.filter(id =loan_id, is_active=True, is_deleted=False).first()
        if loan:
            print(loan)
            payments = LoanPayment.objects.filter(loan=loan, is_active=True, is_deleted=False)
            if payments:
                for payment in payments:
                    print("-----payment")
                    print(payment)

        else:
            print("---nothing")
            return None