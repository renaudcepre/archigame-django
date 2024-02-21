from django.contrib.auth.models import AbstractUser

from games.models import Game, PlayerScore


class User(AbstractUser):
    def score(self, game_pk):
        game = Game.objects.get(pk=game_pk)
        total_score = PlayerScore.objects.filter(game=game, player=self).aggregate(total=Sum('score'))['total']
        return total_score if total_score is not None else 0
