from django import forms
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.contrib.auth import authenticate, login
from django.core.validators import EmailValidator
from backend.models import *
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
                raise forms.ValidationError("Invalid username or password")
            
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
    borrower = forms.RadioSelect()
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
        # widgets = {
        #     'borrower': Select2MultipleWidget(select2_options={
        #         'minimumInputLength': 3,
        #     }),
        # }
        
    def clean(self):
        borrower = self.cleaned_data.get('borrower')
        
        if Loan.objects.filter(Q(borrower=borrower)&Q(status=1)).exists():
            raise forms.ValidationError("This user already have a Loan")
        else:
            pass
        
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(LoanApplicationForm, self).__init__(*args, **kwargs)
        self.fields['borrower'].queryset = Borrower.objects.filter(is_active=True, is_deleted=False)
        self.fields['category'].queryset = LoanCategory.objects.filter(is_active=True, is_deleted=False)
        self.fields['amount'].required = True
        self.fields['repayment_term'].required = True
        self.fields['payment_frequency'].required = True
        self.fields['start_date'].required = True
        self.fields['document'].required = True
        
        
    def save(self, *args, **kwargs):
        form=super(LoanApplicationForm, self).save(*args, **kwargs, commit=False)
        form.user_id = self.user.id
        form.save()
        return form
    
class LoanBorrowerForm(forms.ModelForm):
    """LoanBorrowerForm definition."""

    # TODO: Define form fields here
    class Meta:
        model = Borrower
        fields = [
            'first_name',
            'last_name',
            'nida_number',
            'email',
            'phone',
            'date_of_birth',
            'address',
            'nature_of_employment',
            'picture'
            
        ]
        
        
    def __init__(self, *args, **kwargs):
        super(LoanBorrowerForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required=True
        self.fields['first_name'].widget.attrs['placeholder'] = ""
        self.fields['last_name'].required=True
        self.fields['email'].required=True
        self.fields['phone'].required=True
        self.fields['date_of_birth'].required=True
    
    
        
    # def save(self, *args, **kwargs):
    #     form=super(LoanBorrowerForm, self).save(*args, **kwargs, commit=True)
    #     form.created_by_id = self.created_by.id
    #     form.save()
    #     return form
        
        

        

            
                
            
