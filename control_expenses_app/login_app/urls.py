from django.urls import path
from .views import registration_view, logout_view, login_view, update_profile_view

urlpatterns = [
    path('register/', registration_view, name="registration_view"),
    path('logout/', logout_view, name="logout_view"),
    path('login/', login_view, name="login_view"),
    path('profile/', update_profile_view, name="profile_view"),
]