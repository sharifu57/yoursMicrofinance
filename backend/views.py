from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from backend.forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.db.models import Sum
import pendulum
import random
from backend.models import *
from django.http import HttpResponse
import json
# Create your views here.

class MainView(View):
    @method_decorator(never_cache)
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class LoginView(View):
    def get(self, request, *args, **kwargs):
        
        form=AuthenticationForm()
        
        context={
            'form':form
        }

        return render(request,'authentication/login.html', context)
    
    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(request.POST)

        if form.is_valid():
            print("***valid")
            user = form.login(request)
            if user:
                login(request, user)
                return redirect('dashboard')
                
            else:
                messages.error(request, 'failed')
                return redirect('auth_login')
                
        else:
            print("**not valid")
            messages.error(request, 'failed to Login')
        
            context = {
                'form': form,
                'messages': messages
            }
            return render(request,'authentication/login.html', context)
        

class DashboardView(MainView):
    def get(self, request, *args, **kwargs):
        
        import pendulum
        
        # now = pendulum.now()
        
        
        # start_date = now.start_of('month').date()
        # start_date = pendulum.today()
        # end_date = pendulum.today()
        
        loan_sum = Loan.objects.aggregate(total=Sum('amount'))
        borrowers = Borrower.objects.all()
        new_clients = Borrower.objects.filter(
            is_active=True, 
            is_deleted=False,
            created__date=pendulum.today()
        )
        
      
        context={
            'loan_sum': loan_sum,
            'borrowers': borrowers,
            'new_added': new_clients
        }
        
        return render(request, 'home/dashboard.html', context)
    
    
class CreateNewLoanView(MainView):
    def get(self, request, *args, **kwargs):
        
        form = LoanApplicationForm()
        
        context={
            'form': form
        }
        
        return render(request, 'home/create_loan.html', context)
    

def generate_unique_numbers():
    return random.randint(1000000000, 9999999999)
    
class CreateNewBorrower(MainView):
    def get(self, request, *args, **kwargs):
        form = LoanBorrowerForm()
        context = {
            'form': form
        }
        return render(request, 'home/borrower_form.html', context)


    def post(self, request, *args, **kwargs):
        form = LoanBorrowerForm(
            request.POST
        )
        
        if form.is_valid():
            print("-----a valid form")
            borrower = Borrower()
            borrower.first_name = request.POST['first_name']
            borrower.last_name = request.POST['last_name']
            borrower.email = request.POST['email']
            borrower.phone = request.POST['phone']
            borrower.nida_number = request.POST['nida_number']
            borrower.address = request.POST['address']
            borrower.date_of_birth = request.POST['date_of_birth']
            borrower.nature_of_employment = request.POST['nature_of_employment']
            borrower.picture = request.FILES['picture']
            borrower.created_by = request.user
            borrower.identity = generate_unique_numbers()
        
            borrower.save()  
            print(borrower)   
            
            info = {
                "status": True,
                "message": "Successfully Created"
            }  
            
            return HttpResponse(json.dumps(info)) 
        
        else:
            print("-----not created completely")
            form = LoanBorrowerForm()
            info = {
                "status": False,
                "message": "Failed To Create",
                "Error": form.errors
            }  
            
            return HttpResponse(json.dumps(info))
