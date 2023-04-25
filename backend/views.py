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
        
        loan_sum = Loan.objects.aggregate(total=Sum('amount'))
      
        context={
            'loan_sum': loan_sum
        }
        
        return render(request, 'home/dashboard.html', context)

