from django.contrib.auth.models import User
from viewflow import flow
from viewflow.base import this, Flow
from viewflow.flow.views import CreateProcessView, UpdateProcessView, StartFlowMixin
from backend.models import *


class LoanApplicationFlow(StartFlowMixin):
    start = (
        flow.StartView(
            StartFlowMixin
        ).Permission(auto_create=True).Next()
    )
