from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .forms import NewExpenseModelForm
from .models import Expense

@login_required
def new_expense(request):

    if request.method == 'POST':

        form = NewExpenseModelForm(request.POST)

        if form.is_valid():
            #instance = Expense(**form.cleaned_data)
            form.save()

            return redirect('new_expense')

    else:
        form = NewExpenseModelForm()

    return render(request, "wydatki_app/new_expense.html", {'form': form})