from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [

    path('register/', views.RegisterEmployee.as_view(), name='register'),
    path('verify/', views.VerifyEmployee.as_view(), name='verify'),
    path('apps/', views.ListCreateApplication.as_view(), name='apps'),
    path('approve-app/', views.ApproveApplication.as_view(), name='approve-app'),
    path('update-employee/<pk>/', views.UpdateEmployeeOrganization.as_view(), name='update-employee'),

]
    