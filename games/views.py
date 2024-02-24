import datetime
import json

from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView

from users.models import User
from .forms import GameForm
from .forms import PlayForm
from .models import Game
from .models import GameConfiguration, PlayerScore
from .models import Play


def add_play(request):
    if request.method == 'POST':
        form = PlayForm(request.POST)
        if form.is_valid():
            play = form.save()

            # Extrait et décode les scores JSON
            scores_json = request.POST.get('scores_json', '{}')
            scores = json.loads(scores_json)

            for player_id, score in scores.items():
                # Assure-toi que le score est un entier et traite chaque score
                try:
                    score = int(score)
                    player = User.objects.get(pk=player_id)
                    PlayerScore.objects.update_or_create(
                        play=play,
                        player=player,
                        defaults={'score': score},
                    )
                except (ValueError, TypeError, User.DoesNotExist):
                    continue

            return redirect(reverse_lazy('leaderboards'))
    else:
        form = PlayForm()

    configurations = GameConfiguration.objects.all()
    users = User.objects.all()
    return render(request, 'crud/plays/add_play.html', {
        'form': form,
        'configurations_json': [{"value": config.id, "label": str(config)} for config in configurations],
        'users_json': [{"value": user.id, "label": str(user)} for user in users],
    })


def leaderboards(request):
    game = Game.objects.filter(id=1).first()  # todo: random game
    return render(request, 'leaderboards/leaderboards.html', context={'game': game})


def leaderboard(request, game_id):
    game = Game.objects.filter(id=game_id).first()
    return render(request, 'leaderboards/leaderboards.html', context={'game': game})


def get_leaderboard_for_game(request, game_id):
    game = GameConfiguration.objects.filter(id=game_id).first()
    if not game:
        return JsonResponse({'error': 'Configuration de jeu non trouvée.'}, status=404)

    # Date actuelle
    now = timezone.now()

    # Début de l'année et du mois en cours
    year_start = datetime.datetime(now.year, 1, 1)
    month_start = datetime.datetime(now.year, now.month, 1)

    # Leaderboard pour toutes les périodes
    leaderboard_all_time = PlayerScore.objects.filter(
        play__game_configuration=game
    ).values(
        'player__username'
    ).annotate(
        total_score=Sum('score')
    ).order_by('-total_score')

    # Leaderboard pour l'année en cours
    leaderboard_year = PlayerScore.objects.filter(
        play__game_configuration=game,
        play__date__gte=year_start
    ).values(
        'player__username'
    ).annotate(
        total_score=Sum('score')
    ).order_by('-total_score')

    # Leaderboard pour le mois en cours
    leaderboard_month = PlayerScore.objects.filter(
        play__game_configuration=game,
        play__date__gte=month_start
    ).values(
        'player__username'
    ).annotate(
        total_score=Sum('score')
    ).order_by('-total_score')

    data = {
        'game': game.game.name,
        'extensions': serialize('json', game.extensions.all()),
        'leaderboard_all_time': list(leaderboard_all_time),
        'leaderboard_year': list(leaderboard_year),
        'leaderboard_month': list(leaderboard_month),
    }
    return JsonResponse(data)


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

    return render(request, 'crud/games/add_game.html', {'form': form})


class GameDetailView(DetailView):
    model = Game
    template_name = 'crud/games/detail.html'
    context_object_name = 'game'
    pk_url_kwarg = 'game_id'


class GameUpdateView(UpdateView):
    model = Game
    fields = ['name', 'bgg_number']
    template_name = 'crud/games/update.html'
    success_url = reverse_lazy('game_list')


def game_list(request):
    games = Game.objects.all()
    return render(request, 'crud/games/list.html', {'games': games})
