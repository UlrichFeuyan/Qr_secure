from django.urls import path

from .views import *


app_name = 'personnel'
urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('create_employe/', EmployeCreateView.as_view(), name='create_employe'),
    path('list_employe/', EmployeListView.as_view(), name='list_employe'),
    path('qrscanner/', QrScanner.as_view(), name='qrscanner'),
]
