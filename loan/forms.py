from django import forms
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.contrib.auth import authenticate, login
from django.core.validators import EmailValidator
from loan.models import *
from django.contrib.auth.forms import AuthenticationForm
import random
from django_select2.forms import Select2MultipleWidget  

class AuthenticationForm(forms.ModelForm):
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    class Meta:
        model = User
        fields = ["username","email","password"]


    def clean(self):
        username = str(self.cleaned_data.get("username")).strip().replace(" ", "").lower()
        password = str(self.cleaned_data.get("password")).strip().replace(" ", "").lower()

        if User.objects.filter(Q(username=username)| Q(email=username) | Q(password = password)).exists():
            user_login = User.objects.filter(Q(username=username)|Q(email=username)).first()
            user = authenticate(username = user_login.username, password = password)
            if not user or not user.is_active:
                raise forms.ValidationError("username or password not active")
            
        else:
            raise forms.ValidationError("Invalid username or password")
            

    def login(self, request):
        username = str(self.cleaned_data.get("username")).strip().replace(" ", "").lower()
        password = str(self.cleaned_data.get("password")).strip().replace(" ", "").lower()
        
        if User.objects.filter(Q(username=username) | Q(email=username)).exists():
            user_obj = User.objects.filter(Q(username=username) | Q(email = username)).first()
            user = authenticate(username = user_obj.username, password=password)

        else:
            return None

        return user

    def __init__(self, *args, **kwargs):
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].required = True
        self.fields['password'].required = True 
        


class LoanApplicationForm(forms.ModelForm):
    """Form definition for LoanApplication."""
    class Meta:
        """Meta definition for LoanApplicationform."""

        model = Loan
        fields = [
            'borrower',
            'category',
            'amount',
            'repayment_term',
            'payment_frequency',
            'start_date',
            'document'
        ]
        
    def clean(self):
        cleaned_data = super(LoanApplicationForm, self).clean()
        
    
    
 
   
class LoanBorrowerForm(forms.ModelForm):
    """LoanBorrowerForm definition."""
    # TODO: Define form fields here
    class Meta:
        model = Borrower
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone',
            'nida_number',
            'address',
            'date_of_birth',
            'nature_of_employment',
            'picture',
            
        ]
        
    def __init__(self, *args, **kwargs):
        super(LoanBorrowerForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        
    
    def clean(self, *args, **kwargs):
        cleaned_data = self.cleaned_data
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        
        if Borrower.objects.filter(first_name__iexact = first_name).exists():
            raise forms.ValidationError("user Already exists")
        if not last_name:
            raise forms.ValidationError("this field is required")
        else:
            pass
        
    
    def save(self, *args, **kwargs):
        form = super(LoanBorrowerForm, self).save(*args, **kwargs, commit=False)
        form.save()
        return form
    

class LoanPaymentForm(forms.ModelForm):
    """Form definition for LoanPayment."""

    class Meta:
        """Meta definition for LoanPaymentform."""

        model = LoanPayment
        fields = ['payment_amount','payment_method']
        
    def __init__(self, *args, **kwargs):
        super(LoanPaymentForm, self).__init__(*args, **kwargs)
        self.fields['payment_amount'].required=True
        self.fields['payment_method'].required=True

    def clean(self):
        payment_amount = self.cleaned_data.get('payment_amount')
        payment_method = self.cleaned_data.get('payment_method')
        
        if payment_amount is None:
            self.errors['payment_amount'] = "Please provide this Amount"
            
        
        
    
        
    
        
        

        

            
                
            
