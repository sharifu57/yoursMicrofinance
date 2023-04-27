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
    ),
    path(
        'create_new_loan/',
        views.CreateNewLoanView.as_view(),
        name="create_new_loan"
    ),
    path(
        'add_new_borrower/',
        views.CreateNewBorrower.as_view(),
        name="add_new_borrower"
    )
]