from django.urls import path


from hospital.views import *

urlpatterns = [
    path('item/', ItemList.as_view()),
    path('item/<str:sku>/', ItemDetail.as_view()),
    path('manage/', Manage.as_view()),
    path('order/', OrderList.as_view()),
    path('order/<str:order>/', OrderDetail.as_view()),
    path('recovery/', Recovery.as_view()),
    path('locations/', LocationStock.as_view()),
    path('locations/clear', LocationStock.as_view()),
]