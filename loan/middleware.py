# middleware.py

from django.shortcuts import redirect
from django.urls import reverse

class SessionExpirationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Check if the user is authenticated and their session has expired
        if request.user.is_authenticated and not request.session.get_expiry_age():
            # Redirect to the login page
            return redirect(reverse('auth_login'))

        return response
