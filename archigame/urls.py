
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path
from users.views import profile_view

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/profile/', profile_view, name='profile'),
    path('admin/', admin.site.urls),
]
