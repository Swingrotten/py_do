from django.urls import path
from . import views

app_name = 'shipments'

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_shipment, name='create_shipment'),
    path('list/', views.shipment_list, name='shipment_list'),
    path('detail/<str:tracking_number>/', views.shipment_detail, name='shipment_detail'),
    path('confirm-receipt/<str:tracking_number>/', views.confirm_receipt, name='confirm_receipt'),
] 