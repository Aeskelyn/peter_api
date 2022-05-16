from django.urls import path, include


from callup.views import Status

urlpatterns = [
    path('status/', Status.as_view()),
    path('station/', include('callup.url.station_urls')),
    path('issue/', include('callup.url.issue_urls'))
]
