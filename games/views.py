from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.db.models import Count
from django.shortcuts import render, redirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView

from .forms import GameForm
from .models import Game, UserGameScore, GameConfiguration


def get_cached_game_list():
    game_list = cache.get('game_list')
    if game_list is None or len(game_list) == 0:
        games_with_scores = GameConfiguration.objects.annotate(num_scores=Count('usergamescore')).filter(
            num_scores__gt=0)
        game_list = list(games_with_scores)
        cache.set('game_list', game_list, timeout=None)
    return game_list


def leaderboards(request):
    game_conf_list = get_cached_game_list()
    game_configuration = game_conf_list.pop(0)
    cache.set('game_list', game_conf_list, timeout=None)
    leaderboard = UserGameScore.objects.filter(game_configuration=game_configuration).order_by('-total_score')[:10]

    return render(request, 'leaderboards.html', {'game': game_configuration, 'leaderboard': leaderboard})


@login_required
def add_game(request):
    form = GameForm()
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            game = form.save(commit=False)
            game.save()
            return redirect(reverse('game_detail',
                                    args=[game.id]))
        form = GameForm()

    return render(request, 'games/add_game.html', {'form': form})


class GameDetailView(DetailView):
    model = Game
    template_name = 'games/detail.html'
    context_object_name = 'game'
    pk_url_kwarg = 'game_id'


class GameUpdateView(UpdateView):
    model = Game
    fields = ['name', 'bgg_number']
    template_name = 'games/update.html'
    success_url = reverse_lazy('game_list')


def game_list(request):
    games = Game.objects.all()
    return render(request, 'games/list.html', {'games': games})
