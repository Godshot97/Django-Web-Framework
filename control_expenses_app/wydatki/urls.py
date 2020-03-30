from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('wydatki_app.urls')),
    path('', include('login_app.urls')),
]
