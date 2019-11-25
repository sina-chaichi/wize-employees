from django.urls import path
from . import views

app_name = 'duties'

urlpatterns = [

    path('add-duty/', views.AddDuty.as_view(), name='add-duty'),
    path('update-delete-duty/<pk>/', views.UpdateDeleteDuty.as_view(), name='update-delete-duty'),

]
    