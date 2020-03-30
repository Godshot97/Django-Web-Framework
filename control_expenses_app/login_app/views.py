from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import RegistrationForm, LoginForm, ProfileUpdateForm
from .models import Profile


# REGISTER
def registration_view(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Twoje konto zostało utworzone. Teraz możesz się zalogować.')
            return redirect('login_view')
    else:
        form = RegistrationForm()

    return render(request, 'login_app/register.html', {'form': form})

# LOGOUT
def logout_view(request):
    logout(request)
    return redirect('login_view')

# LOGIN 
def login_view(request):
    user = request.user

    if user.is_authenticated:
        return redirect('new_expense_view')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect('new_expense_view')
    else:
        form = LoginForm()

    return render(request, 'login_app/login.html', {'form': form})


# UPDATE PROFILE
@login_required
def update_profile_view(request):
    user = request.user

    if request.method == "POST":
        form = ProfileUpdateForm(request.POST)

        if form.is_valid():
            profile_to_update = Profile.objects.get(user=user)
            profile_to_update.first_name = request.POST['first_name']
            profile_to_update.last_name = request.POST['last_name']
            if request.POST['monthly_budget'] == '':
                profile_to_update.monthly_budget = 0
            else:
                profile_to_update.monthly_budget = request.POST['monthly_budget']
            profile_to_update.save()
            print("Profile successfully updated!")

    else:
        form = ProfileUpdateForm(
            initial = {
                "first_name": user.profile.first_name,
                "last_name": user.profile.last_name,
                "monthly_budget": user.profile.monthly_budget
            })

    return render(request, 'login_app/profile.html', {"form": form})