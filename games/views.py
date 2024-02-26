import datetime
import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers import serialize
from django.db.models import Sum
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView, CreateView

from users.models import User
from .forms import PlayForm, ExtensionFormSet
from .models import GameConfiguration, PlayerScore


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


from django.shortcuts import render, redirect
from .forms import GameForm
from .models import Game, Extension


def add_game(request):
    if request.method == 'POST':
        game_form = GameForm(request.POST)
        if game_form.is_valid():
            game = game_form.save()

            # Prépare une liste pour stocker les données des extensions
            extensions_data = []
            for key, value in request.POST.items():
                if key.startswith('extension_name_'):
                    _, idx = key.rsplit('_', 1)
                    extension_data = {'name': value, 'bgg_number': None}
                    extensions_data.append((idx, extension_data))
                elif key.startswith('extension_bgg_number_'):
                    _, idx = key.rsplit('_', 1)
                    for extension in extensions_data:
                        if extension[0] == idx:
                            extension[1]['bgg_number'] = value or None
                            break

            # Crée les objets Extension
            for _, data in extensions_data:
                if data['name']:  # Assure que le champ d'extension n'est pas vide
                    Extension.objects.create(game=game, name=data['name'], bgg_number=data['bgg_number'])

            return redirect('game_detail', pk=game.pk)
    else:
        game_form = GameForm()

    return render(request, 'games/add_game.html', {'form': game_form})


class GameCreateView(LoginRequiredMixin, CreateView):
    model = Game
    form_class = GameForm
    template_name = 'games/add_game.html'
    success_url = reverse_lazy('game_list')

    def get_context_data(self, **kwargs):
        context = super(GameCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['extensions_form'] = ExtensionFormSet(self.request.POST)
        else:
            context['extensions_form'] = ExtensionFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        extensions_form = context['extensions_form']
        if extensions_form.is_valid():
            self.object = form.save()
            extensions_form.instance = self.object
            extensions_form.save()
            return super(GameCreateView, self).form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class GameDetailView(DetailView):
    model = Game
    template_name = 'games/detail.html'
    context_object_name = 'game'
    pk_url_kwarg = 'game_id'


class GameUpdateView(LoginRequiredMixin, UpdateView):
    model = Game
    form_class = GameForm
    template_name = 'games/update_game.html'
    success_url = reverse_lazy('game_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            formset = ExtensionFormSet(self.request.POST, instance=self.object)
            if not formset.is_valid():
                print(formset.errors)  # Affiche les erreurs pour diagnostic
            context['extensions_form'] = ExtensionFormSet(self.request.POST, instance=self.object)

        else:
            context['extensions_form'] = ExtensionFormSet(instance=self.object)
        # print(f"CONTEXT: {context}")
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        extensions_form = context['extensions_form']
        if extensions_form.is_valid():
            self.object = form.save()
            for form in extensions_form.forms:
                if form.cleaned_data.get('id') and form.cleaned_data.get('deleted'):
                    print('delETR')
                    Extension.objects.filter(id=form.cleaned_data['id']).delete()
            extensions_form.instance = self.object
            extensions_form.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))


def game_list(request):
    games = Game.objects.all()
    return render(request, 'games/list.html', {'games': games})
