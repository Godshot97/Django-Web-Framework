from django.shortcuts import render, redirect
#from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages # flash messages
from .forms import CustomUCF, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required 

def register(request):
    if request.method == 'POST':
        form = CustomUCF(request.POST) 
        if form.is_valid():
            form.save() 
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are able to log in now.')
            return redirect('login')
    else:
        form = CustomUCF()
    return render(request, 'users_app/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':    
        u_form = UserUpdateForm(request.POST, instance=request.user) # populate form by current information about given user
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile) 

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user) 
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users_app/profile.html', context)