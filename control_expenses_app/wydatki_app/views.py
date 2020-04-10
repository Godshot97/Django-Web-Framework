from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .forms import NewExpenseModelForm
from .models import Expense

@login_required
def home(request):
    user = request.user

    if request.method == 'POST':

        form = NewExpenseModelForm(request.POST)
        form.instance.owner = user

        if form.is_valid():
            #instance = Expense(**form.cleaned_data)
            form.save()

            return redirect('home_view')

    else:
        form = NewExpenseModelForm()

    expenses = Expense.objects.filter(owner=user).order_by('-purchase_date')

    return render(request, "wydatki_app/home.html", {'form': form, 'expenses': expenses})
