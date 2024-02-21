from django.contrib.auth.models import AbstractUser
from django.db import models

from games.models import Game, PlayerScore


class User(AbstractUser):
    coucou = models.IntegerField(default=0)

