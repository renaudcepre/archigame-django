from django.db.models import Count
from django.shortcuts import render

from .models import Game, UserGameScore


def leaderboards(request):
    count = Game.objects.annotate(num_scores=Count('usergamescore')).filter(num_scores__gt=0).count()

    if count > 0:
        game = Game.objects.annotate(num_scores=Count('usergamescore')).filter(num_scores__gt=0).order_by('?')[
               :1].get()
        leaderboard = UserGameScore.objects.filter(game=game).order_by('-total_score')[:10]
    else:
        game = None
        leaderboard = []

    return render(request, 'leaderboards.html', {'game': game, 'leaderboard': leaderboard})
