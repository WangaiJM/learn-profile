from django.urls import path, include
from . import views

urlpatterns = [
    path('doctor-login/', views.doctor_login, name='doctor-login')
]
