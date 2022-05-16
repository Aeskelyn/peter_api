from django.urls import path

from callup.view.issue_view import *

urlpatterns = [
    path('open/', OpenIssue.as_view()),
    path('resolve/', ResolveIssue.as_view()),
    path('report/', ReportIssue.as_view()),
]
