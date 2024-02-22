from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Sum

from games.models import Game, PlayerScore, UserGameScore, Play


class User(AbstractUser):
    coucou = models.IntegerField(default=0)

    def total_score(self):
        return UserGameScore.objects.filter(user=self).aggregate(total=Sum('total_score'))['total'] or 0

    def total_plays(self):
        return Play.objects.filter(players=self).count()
