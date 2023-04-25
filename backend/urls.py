from django.urls import path
from . import views

urlpatterns = [
    path(
        '', 
        views.LoginView.as_view(),
        name="auth_login"
    ),
    path(
        'auth_login/',
        views.LoginView.as_view(),
        name="auth_login"
    ),
    path(
        'dashboard/',
        views.DashboardView.as_view(),
        name="dashboard"
    )
]