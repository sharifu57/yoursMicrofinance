from django.contrib import admin
from backend.models import *

# Register your models here.
admin.site.register(Borrower)
admin.site.register(LoanCategory)
admin.site.register(Loan)
admin.site.register(Application)
admin.site.register(LoanPayment)