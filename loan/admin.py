from django.contrib import admin
from loan.models import *
from river.models import TransitionApproval

# Register your models here.
admin.site.register(Borrower)
admin.site.register(LoanCategory)
admin.site.register(Loan)
admin.site.register(Application)
admin.site.register(LoanPayment)
admin.site.register(TransitionApproval)