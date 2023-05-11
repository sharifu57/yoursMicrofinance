from django.shortcuts import render
from django.views.generic import View
from loan.views import MainView
# Create your views here.

class HomeView(MainView):
    def get(self, request, *args, **kwargs):
        
        return render(render, 'home/index.html')
        
