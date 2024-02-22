from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include

from games.views import leaderboards, add_game, GameDetailView, GameUpdateView, game_list
from users.views import profile_view

urlpatterns = [
    path('leaderboards/', leaderboards, name='leaderboards'),
    path("accounts/", include("django.contrib.auth.urls")),
    path('accounts/profile/', profile_view, name='profile'),
    path('admin/', admin.site.urls),
    path('games/add', add_game, name='add_game'),
    path('games/', game_list, name='game_list'),
    path('games/update_game/<int:pk>/', GameUpdateView.as_view(), name='update_game'),
    path('games/detail/<int:game_id>/', GameDetailView.as_view(), name='game_detail')
]
