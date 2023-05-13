from viewflow.flow.views import CreateProcessView, StartProcessViewMixin
from viewflow.flow.views.utils import get_next_task
from viewflow import flow
from viewflow.base import this, Flow
from loan.models import Loan
from loan.views import * 
from viewflow.flow.views import StartFlowMixin
from viewflow.models import Process


class LoanApplicationFlow(Flow):
    start = flow.Start(
        StartFlowMixin,
        fields = [],
        task_title = 'Start this flow'
    ).Next(
        this.review_the_application
    )
    
    review_the_application = flow.View(
        your_view_class,
        task_title='Review Loan'
    ).Next(
        this.end
    )
    
    end = flow.End()
    

class StartFlowMixin(StartProcessViewMixin):
    task_class = None

    def activation_done(self, activation):
        next_task = get_next_task(activation.process)
        activation.done()
        if next_task:
            next_task.prepare(activation.process)

class StartLoanFlowView(CreateProcessView, StartFlowMixin):
    pass
