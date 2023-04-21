from django.db import models

# Create your models here.
class MainModel(models.Model):
    is_active = models.BooleanField(null=True, blank=True, default=True)
    is_deleted = models.BooleanField(null=True, blank=True, default=False)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def softdelete(self):
        self.is_deleted = True
        self.is_active = False
        self.updated = pendulum.now()
        self.save()

    class Meta:
        abstract = True
        
NATURE_OF_ACTIVITY = (
    (1, 'Employed'),
    (2, 'Not Employed')
)
    
class Borrower(MainModel):
    customer_Id = models.CharField(max_length=200, null=True, blank=True)
    fist_name = models.CharField(max_length=200, null=True, blank=True)
    middle_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    nida_number = models.CharField(null=True, blank=True)
    address = models.CharField(null=True, blank=True)
    nature_of_employment = models.IntegerField(default=1, choices=NATURE_OF_ACTIVITY, null=True, blank=True) 
    picture = models.ImageField(upload_to='picture/%Y/%m/%d', blank=True, null=True)
    
    def __str__(self):
        return f"{self.fist_name}, ' ' ,{self.last_name}"
    
LOAN_PURPOSES = (
    ('education', 'Education Purpose'),
    ('small_business', 'Business Purpose'),
    ('Agriculture', 'Agriculture'),
    ('other', 'Other')
)

class LoanCategory(MainModel):
    category_name = models.CharField(max_length=200, null=True, blank=True)
    interest = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    repayment_term_range = models.IntegerField(null=True, blank=True)
    loan_amount_range = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    collateral = models.CharField(max_length=300, null=True, blank=True)
    loan_purpose = models.CharField(choices=LOAN_PURPOSES, default=1, null=True, blank=True)
    # for late repayment
    penalty_fee = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True) 
    
    def __str__(self):
        
        return self.category_name 
    
PAYMENT_FREQUENCY = (
    (1, 'Weekly'),
    (2, 'Bi-Weekly'),
    (3, 'Monthly'),
    
)

LOAN_STATUS = (
    (1, 'Active'),
    (2, 'Approved'),
    (3, 'Rejected'),
    (4, 'Waiting')
)

REPAYMENT_TERM = (
    (1, '1 Month'),
    (2, '3 Months'),
    (3, '6 Months'),
    (4, '1 Year')
)

class Loan(MainModel):
    borrower_id = models.ForeignKey('backend.Borrower', on_delete=models.CASCADE, null=True, blank=True)
    category_id = models.ForeignKey("backend.LoanCategory", on_delete=models.SET_NULL)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    interest_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    repayment_term = models.IntegerField(choices=REPAYMENT_TERM, null=True, blank=True)
    payment_frequency = models.IntegerField(choices=PAYMENT_FREQUENCY, null=True, blank=True, default=1)
    interest_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    document = models.FileField(upload_to='documents/%Y/%m/%d', null=True, blank=True)
    status = models.IntegerField(choices=LOAN_STATUS, null=True, blank=True)

    def __str__(self):
        
        return self.amount
    

LOAN_APPLICATIONS = (
    (1, 'Approved'),
    (2, 'Rejected'),
    (3, 'Missing')
)
class Applications(MainModel):
    loan = models.ForeignKey('backend.Loan', on_delete=models.CASCADE, null=True, blank=True)
    status = models.IntegerField(choices=LOAN_APPLICATIONS, null=True, blank=True)
    
    def __str__(self):
        
        return self.loan.id
    
    
PAYMENT_STATUS = (
    (1, 'Paid'),
    (2, 'Pending'),
    (3, 'Late')
) 

class LoanPayment(MainModel):
    loan = models.IntegerField('backend.Loan', null=True, blank=True, on_delete=models.CASCADE)
    payment_number = models.CharField(max_length=200, null=True, blank=True)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # the amount that lowers the loan balance of a customer amount
    principal_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) 
    # This is the cumulative amount of interest paid up to the current payment.
    total_interest_paid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # This is the cumulative amount of principal paid up to the current payment.
    total_principal_paid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    remaining_balance = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    payment_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    late_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.IntegerField(choices=PAYMENT_STATUS, null=True, blank=True)
    
    def __str__(self):
        
        return self.payment_number
