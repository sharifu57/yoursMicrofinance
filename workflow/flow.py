from viewflow import flow
from viewflow.base import this, Flow
from loan.models import Loan
from loan.views import *
from viewflow.flow.views import StartFlowMixin
from viewflow.models import Process


# class LoanApplicationFlow(flow.Flow):
#     start = flow.start(my_view).Next(this.task)
#     task = flow.Handler(perform_task).Next(this.check_status)
#     check_status = flow.If(this.is_completed).then(this.end).Else(this.task)
#     end = flow.end()

class LoanApprovalFlow(Flow):
    process_class = Loan
    lock_impl = None
    
    start = flow.StartFunction(this.CreateNewLoanView).Next(this.approval_or_reject)
    
    approval_or_reject = flow.View(
        LoansView,
        task_description = "Review the Loan Application" 
    ).Permission(auto_correct=True).Next(this.check_approval)
    
    check_approval = flow.If(
        cond=lambda act: act.process.is_approved,
        task_title="Loan Approved"
    ).Then(
        this.end
    ).Else(
        this.reject_loan
    )
    
    @classmethod
    def reject_loan_action(cls, activation):
        activation.process.status=='3'
        activation.process.save()