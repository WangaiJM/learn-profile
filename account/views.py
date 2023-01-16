from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.http import HttpResponse


def doctor_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(employee_number=username, password=password)
            if user is not None:
                if user.is_doctor:
                    login(request, user)
                    return redirect("doctor-dashboard")
                else:
                    return HttpResponse("Unauthorized", status=401)
            else:
                print("not a user")
        else:
            print("no clue")

    form  = AuthenticationForm()
    context = {'login_form': form}
    return render(request, 'login/doctor_login.html', context)
