from django.urls import path
from . import views

app_name = 'logistics'

urlpatterns = [
    path('record/create/<str:tracking_number>/', views.create_record, name='create_record'),
    path('records/<str:tracking_number>/', views.record_list, name='record_list'),
    path('tasks/', views.task_list, name='task_list'),
] 