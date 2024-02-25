from django.urls import path

from games.views import GameCreateView, GameDetailView, GameUpdateView, game_list, leaderboards, leaderboard, add_play

urlpatterns = [
    # Crud
    path('games/add', GameCreateView.as_view(), name='add_game'),
    path('games/', game_list, name='game_list'),
    path('games/update_game/<int:pk>/', GameUpdateView.as_view(), name='update_game'),
    path('games/detail/<int:game_id>/', GameDetailView.as_view(), name='game_detail'),

    path('plays/add/', add_play, name='add_play'),
    # Leaderboards
    path('leaderboards/', leaderboards, name='leaderboards'),
    path('leaderboards/<int:game_id>', leaderboard, name='leaderboards_detail'),

]
