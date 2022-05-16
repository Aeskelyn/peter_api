from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.authtoken import views as va
from . import views

urlpatterns = [
    path('token-auth/', va.obtain_auth_token),
    path('callup/', include('callup.urls')),
    path('logout/', views.Logout.as_view()),
    path('hospital/', include('hospital.urls')),
    path('doc/', TemplateView.as_view(template_name='api.html'))
]