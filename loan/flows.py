from viewflow import flow
from viewflow.base import this, Flow
from viewflow.flow.views import StartFlowMixin
from django.contrib.auth.models import Group
from loan.models import *
from loan.views import *

class LoanApplicationFlow(Flow):
    process_class = Loan
    
    start = flow.Start(
        StartFlowMixin
    ).Next(
        this.collect_applicant_information
    )
    
    collect_applicant_information = flow.View(
        views.CreateNewLoanView
    ).Next(
        this.review_creditworthiness
    )
    
    review_creditworthiness = flow.Task(
        views.ViewOneLoan,
        assignees = flow.Function(lambda activation: get_roles('credit officer'))
    ).Next(
        this.approve_loan
    )
    
    approve_loan = flow.Task(
        views.ApproveLoanTask,
        assignees = flow.Function(lambda activation: get_roles('loan managers'))
    ).Next(
        this.end
    )
    
    end = flow.End()
    
    
def get_roles(group_name):
    try:
        group = Group.objects.get(name=group_name)
        return group.user_set.all()
    except Group.DoesNotExist:
        return []
    