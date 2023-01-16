from django.urls import path
from . import views

urlpatterns = [
    path('dashboard-doctor/', views.dashboard_doctor, name='doctor-dashboard')
]
