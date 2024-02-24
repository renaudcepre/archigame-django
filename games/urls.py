from django.urls import path, include

from games.views import add_game, GameDetailView, GameUpdateView, game_list, leaderboards, leaderboard

urlpatterns = [
    # Crud
    path('games/add', add_game, name='add_game'),
    path('games/', game_list, name='game_list'),
    path('games/update_game/<int:pk>/', GameUpdateView.as_view(), name='update_game'),
    path('games/detail/<int:game_id>/', GameDetailView.as_view(), name='game_detail'),



    # Leaderboards
    path('leaderboards/', leaderboards, name='leaderboards'),
    path('leaderboards/<int:game_id>', leaderboard, name='leaderboards_detail'),

]
