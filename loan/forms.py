from django import forms
from django.contrib.auth.models import User, Group, Permission
from django.db.models.query_utils import Q
from django.contrib.auth import authenticate, login
from django.core.validators import EmailValidator
from loan.models import *
from django.contrib.auth.forms import AuthenticationForm
import random
from django_select2.forms import Select2MultipleWidget  
import pendulum
from datetime import date, timedelta

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
    
    def __init__(self, *args, **kwargs):
        super(LoanApplicationForm, self).__init__(*args, **kwargs)
        self.fields['borrower'].required = True
        
        
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
            'middle_name',
            'email',
            'phone',
            'nida_number',
            'address',
            'date_of_birth',
            'picture',
            
        ]
        
    def __init__(self, *args, **kwargs):
        super(LoanBorrowerForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['middle_name'].required = True
        self.fields['email'].required = True
        self.fields['phone'].required = True
        self.fields['nida_number'].required = True
        self.fields['address'].required = True
        self.fields['date_of_birth'].required = True
        self.fields['picture'].required = False
        
    
    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        today  = date.today()
        age_limit_today = today - timedelta(days=18 * 365)
        
        if date_of_birth > age_limit_today:
            raise forms.ValidationError("You must be at least 18 years old.")
        return date_of_birth
        
    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        
        if Borrower.objects.filter(first_name__icontains=first_name).exists():
            raise forms.ValidationError("This First Name already exists")
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")
        
        if Borrower.objects.filter(first_name__icontains=last_name).exists():
            raise forms.ValidationError("This Last Name already exists")
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        
        if Borrower.objects.filter(email__icontains=email).exists():
            raise forms.ValidationError("This Email already exists")
        
    def clean_nida_number(self):
        nida_number = self.cleaned_data.get("nida_number")
        
        if len(nida_number) != 20:
            raise forms.ValidationError("Nida Number must be at least 20 characters")
        
    
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
            
            

class RoleForm(forms.ModelForm):
    """Form definition for Role."""
    class Meta:
        """Meta definition for Roleform."""
        model = Group
        fields = ['name']
        
        
    def clean(self):
        if hasattr(self.instance, 'pk'):
            if Group.objects.filter(
                    name__iexact=self.cleaned_data.get("name")).exclude(
                        id=self.instance.pk).exists():
                self._errors[
                    'name'] = f"{self.cleaned_data.get('name')} Already Taken"
        else:
            if Group.objects.filter(
                    name__iexact=self.cleaned_data.get("name")).exists():
                self._errors[
                    'name'] = f"{self.cleaned_data.get('name')} Already Taken"
        return self.cleaned_data
        
    
    def __init__(self, *args, **kwargs):
        super(RoleForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = True
    

        
        
    
        
    
        
        

        

            
                
            
