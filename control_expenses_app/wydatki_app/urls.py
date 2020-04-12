from django.contrib import admin
from django.urls import path, include
from .views import home, del_expense, update_expense

urlpatterns = [
    path('home/', home, name="home_view"),
    path('home/del_expense/<int:pk>/', del_expense, name="del_expense_view"),
    path('home/update_expense/<int:pk>/', update_expense, name="update_expense_view"),
]