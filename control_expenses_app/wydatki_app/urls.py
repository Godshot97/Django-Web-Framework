from django.contrib import admin
from django.urls import path, include
from .views import new_expense

urlpatterns = [
    path('new/', new_expense, name="new_expense_view"),
]