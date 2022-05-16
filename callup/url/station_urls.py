from django.urls import path, include


from callup.view.station_view import *

urlpatterns = [
    path('login/', LoginStation.as_view()),
    path('logout/', LogoutStation.as_view()),
    path('report/', ReportStationType.as_view()),
    path('report/<str:station_type>/', ReportStation.as_view()),
    path('report/<str:station_type>/<str:line>', ReportLine.as_view()),
]
