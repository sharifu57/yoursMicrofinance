from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from backend.forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum
import pendulum
import random
from backend.models import *
from django.http import HttpResponse, JsonResponse
import json
import pendulum
from django.conf import settings
from django.core.paginator import Paginator
from django.contrib.postgres.search import SearchVector

# Create your views here.

class MainView(View):
    @method_decorator(never_cache)
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class LogoutView(MainView):
    def get(self, request):
        # Do some stuff
        logout(request)
        # Redirect to some page
        return redirect('auth_login')

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
        title = "Dashboard OverView"
        identity_number = None
        
        loan_sum = Loan.objects.aggregate(total=Sum('amount'))
        interest_amount = Loan.objects.aggregate(total=Sum('interest_amount'))
        borrowers = Borrower.objects.filter(is_active=True, is_deleted=False)
        
        if borrowers:
            for borrower in borrowers:
                if borrower.identity is None:
                    borrower.identity = generate_unique_numbers()
                    borrower.save()
                    
        
        revenue_amount = loan_sum['total'] + interest_amount['total']
        
        members = Borrower.objects.all().count()
        
        loan_data = Loan.objects.values('amount', 'borrower__first_name').order_by('-created')[:6]
        payment_data = LoanPayment.objects.values('payment_amount', 'loan__amount').order_by('-created')[:6]
        loan_json = json.dumps(
            list(loan_data), 
            indent=4, 
            sort_keys=True, 
            default=str
        )
        payment_json = json.dumps( 
            list(payment_data),
            indent=4, 
            sort_keys=True, 
            default=str
        )
        
        print("****payment json")
        print(payment_json)
        context = {
            'title': title,
            'revenue_amount': revenue_amount,
            'members': members,
            'loan_sum': loan_sum,
            'interest_amount': interest_amount,
            'loan_data': loan_json,
            'payment_data': payment_json
        }
        
        return render(request, 'home/dashboard.html', context)
        

class LoanBookView(MainView):
    def get(self, request, *args, **kwargs):
        
        import pendulum
    
        loan_sum = Loan.objects.aggregate(total=Sum('amount'))
        borrowers = Borrower.objects.all()
        new_clients = Borrower.objects.filter(
            is_active=True, 
            is_deleted=False,
            created__date=pendulum.today()
        )
        
        loans = Loan.objects.filter(
            is_active=True, 
            is_deleted=False
        ).order_by('-created')[:3]
      
        context={
            'loan_sum': loan_sum,
            'borrowers': borrowers,
            'new_added': new_clients,
            'loans': loans
        }
        
        return render(request, 'home/loan_book.html', context)
    

def generate_unique_numbers():
    return random.randint(1000000000, 9999999999)

def generate_payment_number():
    return random.randint(1000000000, 9999999999)
    
class CreateNewBorrower(MainView):
    def get(self, request, *args, **kwargs):
        form = LoanBorrowerForm()
        context = {
            'form': form
        }
        return render(request, 'home/borrower_form.html', context)


    def post(self, request, *args, **kwargs):
        context = list()
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
            borrower.refresh_from_db()
            print(borrower)   
            
            info = {
                "status": True,
                "message": "Successfully Created"
            }  
            context.append(info)
            return HttpResponse(json.dumps(info)) 
        
        else:
            print("-----not created completely")
            info = {
                "status": False,
                "message": "Failed To Create, Some fields are empty"
            }  
            
            return HttpResponse(json.dumps(info))
        
class CreateNewLoanView(MainView):
    def get(self, request, *args, **kwargs):
        
        form = LoanApplicationForm()
        
        context={
            'form': form
        }
        
        return render(request, 'home/create_loan.html', context)
    
    def post(self, request, *args, **kwargs):
        interest_rate = 30
        new_date = None
        form = LoanApplicationForm(
            request.POST
        )
        
        borrower_id = request.POST.get('borrower', None)
        category_id = request.POST.get('category', None)
 
        if form.is_valid():
            loan = Loan()
            loan.amount = request.POST['amount']
            if borrower_id:
                loan.borrower = Borrower.objects.get(id=borrower_id)
            else:
                pass
                
            if category_id:
                loan.category = LoanCategory.objects.get(id=category_id)
            else:
                pass
            loan.repayment_term = request.POST['repayment_term']
            loan.payment_frequency = request.POST['payment_frequency']
            loan.start_date = request.POST['start_date']
            if loan.start_date:
                if loan.repayment_term == "1":
                    loan.end_date = pendulum.parse(loan.start_date).add(months=1).to_date_string()
                    
                if loan.repayment_term == "2":
                    loan.end_date = pendulum.parse(loan.start_date).add(months=3).to_date_string()
                    
                if loan.repayment_term == "3":
                    loan.end_date = pendulum.parse(loan.start_date).add(months=6).to_date_string()
                    
                if loan.repayment_term == "4":
                    loan.end_date = pendulum.parse(loan.start_date).add(years=1).to_date_string()
                    
                else:
                    pass
            else:
                loan.start_date = pendulum.today().to_date_string()
            loan.document = request.FILES['document']
            loan.created_by = request.user
            loan.interest_amount = float(loan.amount) * (interest_rate/100)

            loan.save()
            loan.refresh_from_db()
            
            print("----loan")
            
            info = {
                "status":True,
                "message": "Success created"
            }
            
            return HttpResponse(json.dumps(info))
        
        else:
            form = LoanBorrowerForm()
            info = {
                "status": False,
                "message": "Failed to Create"
            }
            
            return HttpResponse(json.dumps(info))
        
class LoansView(MainView):
    def get(self, request, *args, **kwargs):
        amount = None
        interest_rate = None
        total_interest_amount = None
        loans  = Loan.objects.filter(is_active=True, is_deleted=False).order_by('-created')
        search = request.GET.get('search', None)
        page = request.GET.get('page', 1)
        
        if loans:
            for loan in loans:
                amount = loan.amount
                interest_rate = loan.interest_rate
                if total_interest_amount is None:
                    total_interest_amount = float(amount) + float(float(amount) * float(interest_rate)/100)
                    loan.total_interest_amount = total_interest_amount
                    loan.save()
                    
                else:
                    pass
        
        if request.GET.get('search'):
            loans = loans.annotate(
                search=SearchVector(
                    'amount',
                    'borrower__first_name',
                    'borrower__last_name',
                    'status'
                )
            ).filter(search=search)
            
        paginator = Paginator(loans, 10)
      
        context = {
            'loans': paginator.page(page),
            'search': search
        }
        
        return render(request, 'home/loans.html', context)
    
class ViewOneLoan(MainView):
    def get(self, request, *args, **kwargs):
        
        loan = Loan.objects.get(
            id=self.kwargs.get('loan')
        )
        payment = LoanPayment.objects.filter(
            is_active=True,
            is_deleted=False,
            loan = loan
        ).order_by('-created')
        
        loans = Loan.objects.filter(
            is_active=True, 
            is_deleted=False,
            id=self.kwargs.get('loan')
        )
        payment_sum = payment.aggregate(total=Sum('payment_amount'))
        loan_sum = loans.aggregate(total=Sum('amount'))
    
        try:     
            remaining_amount = loan_sum['total'] - payment_sum['total']
        except(TypeError, KeyError) as e:
            print(f"An error occurred while calculating the remaining amount: {str(e)}")
            remaining_amount = None
        
        context = {
            'loan': loan,
            'payment': payment,
            'payment_sum': payment_sum,
            'remaining_amount': remaining_amount
        }
        
        return render(request, 'home/view_loan.html', context)
    
    
class CreatePaymentView(MainView):
    def get(self, request, *args, **kwargs):
        form = LoanPaymentForm()
        loan_id = kwargs.get('loan')
        if loan_id:
            loan_id=loan_id
            
            
        context = {
           'form': form,
           'loan_id': loan_id
        }
        return render(request, 'home/create_payment.html', context)
    
    def post(self, request, *args, **kwargs):
        form = LoanPaymentForm(
            request.POST
        )       
     
        loan_id = kwargs.get('loan')
        if loan_id:
            loan_id=loan_id
            
    
        if form.is_valid():
            payment = LoanPayment()
            loan = Loan.objects.get(id=loan_id)
            payment.payment_amount = request.POST['payment_amount']
            payment.payment_method = request.POST['payment_method']
            payment.loan = Loan.objects.get(id=loan_id) 
            payment.principal_amount = float(loan.amount) - float(payment.payment_amount)
            payment.payment_number = generate_payment_number()
            payment.save()
            payment.refresh_from_db()
            info = {
                'status': True,
                'message': 'Success Created'
            }
            
            return HttpResponse(json.dumps(info))
        
        info = {
            'status': False,
            'message': 'Failed to Create Payment'
        }
        return HttpResponse(json.dumps(info))
    
    
class ConfirmLoan(MainView):
    def get(self, request, *args, **kwargs):
        loan = Loan.objects.get(id=self.kwargs.get('loan'))
        loan.status = 2
        loan.save()
        
        info = {
            'status': True,
            'message': 'Loan Approved'
        }
        return HttpResponse(json.dumps(info))
    
class RejectLoan(MainView):
    def get(self, request, *args, **kwargs):
        loan = Loan.objects.get(id=self.kwargs.get('loan'))
        loan.status = 3
        loan.save()
        
        info = {
            'status':True,
            'message': 'Loan Rejected'
        }
        return HttpResponse(json.dumps(info))
    
class MembersView(MainView):
    def get(self, request, *args, **kwargs):
        borrowers = Borrower.objects.all()
        
        context = {
            'borrowers': borrowers
        }
        return render(request, 'home/members.html', context)
    

class ReportView(MainView):
    def get(self, request, *args, **kwargs):
    
        if 'start_date' in request.GET:
            start_date = request.GET.get('start_date', None)
            print("*****start_date")
            print(start_date)
            if start_date:
                start_date = pendulum.from_format(start_date, 'YYYY-MM-DD')
            else:
                None
                
        else:
            print("-------no data")
                
        if 'end_date' in request.GET:
            end_date = request.GET.get('end_date', None)
            print("*****start_date")
            print(end_date)
            if end_date:
                end_date = pendulum.from_format(end_date, 'YYYY-MM-DD')
            else:
                None
        else:
            print("-------none data")
            
            
        context = {
            "system_path": settings.DOCUMENT_SYSTEM_IP
        }
    
        return render(request, 'home/report.html', context)
    
    

    


    
        
        
        
        
