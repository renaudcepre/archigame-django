from django.contrib import admin
from django.urls import path, include

from games.views import add_game, GameDetailView, GameUpdateView, game_list, get_leaderboard_for_game, leaderboards, \
    all_games_configurations
from users.views import profile_view

urlpatterns = [
    path('api/leaderboard/<int:game_id>/', get_leaderboard_for_game, name='api_leaderboard_for_game'),
    path('leaderboards/', leaderboards, name='leaderboards'),
    path('api/gameconfigurations/', all_games_configurations, name='games_configurations'),

    path("accounts/", include("django.contrib.auth.urls")),
    path('accounts/profile/', profile_view, name='profile'),
    path('admin/', admin.site.urls),
    path('games/add', add_game, name='add_game'),
    path('games/', game_list, name='game_list'),
    path('games/update_game/<int:pk>/', GameUpdateView.as_view(), name='update_game'),
    path('games/detail/<int:game_id>/', GameDetailView.as_view(), name='game_detail')
]
