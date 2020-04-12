from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test

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


def del_expense(request, pk):
    obj = Expense.objects.get(pk=pk)
    if obj.owner == request.user:
        obj.delete()

    return redirect('home_view')


def update_expense(request, pk):
    user = request.user
    obj = Expense.objects.get(pk=pk)
    
    if obj.owner == user:
        if request.method == 'POST':
            form = NewExpenseModelForm(request.POST)
            form.instance.owner = obj.owner

            if form.is_valid():
                obj.name = form.cleaned_data['name']
                obj.price = form.cleaned_data['price']
                obj.category = form.cleaned_data['category']
                obj.purchase_date = form.cleaned_data['purchase_date']
                obj.save()
                return redirect('home_view')
        
        else:
            initial_data = {
                'name': obj.name,
                'price': obj.price,
                'category': obj.category,
                'purchase_date': obj.purchase_date
            }
            form = NewExpenseModelForm(initial=initial_data)
        
        expenses = Expense.objects.filter(owner=user).order_by('-purchase_date')
    else:
        return redirect('home_view')

    return render(request, "wydatki_app/update_expense.html", {'form': form, 'expenses': expenses})