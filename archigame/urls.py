from django.contrib import admin
from django.urls import path, include
from users.views import profile_view

urlpatterns = [
    path('', include('games.urls')),
    path("accounts/", include("django.contrib.auth.urls")),
    path('accounts/profile/', profile_view, name='profile'),
    path('admin/', admin.site.urls),

]
