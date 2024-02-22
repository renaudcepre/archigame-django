from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.db.models import Count
from django.shortcuts import render, redirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView

from .forms import GameForm
from .models import Game, UserGameScore


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
    template_name = 'games/detail.html'  # Nom du template pour afficher les détails du jeu
    context_object_name = 'game'  # Nom de l'objet contextuel dans le template (facultatif)
    pk_url_kwarg = 'game_id'  # Nom du paramètre dans l'URL qui contient l'ID du jeu


class GameUpdateView(UpdateView):
    model = Game
    fields = ['name', 'bgg_number', 'score_min', 'score_max']  # Champs que vous voulez mettre à jour
    template_name = 'games/update.html'  # Template pour le formulaire de mise à jour
    success_url = reverse_lazy('game_list')  # URL à rediriger après la mise à jour réussie


def game_list(request):
    games = Game.objects.all()
    return render(request, 'games/list.html', {'games': games})
