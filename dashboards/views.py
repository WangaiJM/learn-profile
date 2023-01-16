from django.shortcuts import render

def dashboard_doctor(request):
    return render(request, 'doctor-dashboard.html')
