from django.db.models import Count
from django.shortcuts import render

from .models import Game, UserGameScore

from django.core.cache import cache


def get_cached_game_list():
    game_list = cache.get('game_list')
    if game_list is None or len(game_list) == 0:
        games_with_scores = Game.objects.annotate(num_scores=Count('usergamescore')).filter(num_scores__gt=0)
        game_list = list(games_with_scores)
        cache.set('game_list', game_list, timeout=None)  # Aucune expiration du cache
    return game_list


def leaderboards(request):
    game_list = get_cached_game_list()
    if game_list:
        game = game_list.pop(0)
        # Met à jour la liste des jeux en cache
        cache.set('game_list', game_list, timeout=None)  # Aucune expiration du cache
        leaderboard = UserGameScore.objects.filter(game=game).order_by('-total_score')[:10]

    return render(request, 'leaderboards.html', {'game': game, 'leaderboard': leaderboard})
