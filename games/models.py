from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Game(models.Model):
    name = models.CharField(max_length=255, unique=True)
    bgg_number = models.IntegerField(null=True, blank=True, unique=True)

    def __str__(self):
        return self.name


class Extension(models.Model):
    game = models.ForeignKey(Game, related_name='extensions', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    bgg_number = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class GameConfiguration(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    extensions = models.ManyToManyField(Extension, blank=True)
    min_players = models.IntegerField(default=1)
    max_players = models.IntegerField(default=4)
    score_min = models.IntegerField(default=0)
    score_max = models.IntegerField()

    class Meta:
        ordering = ['game__name']

    def __str__(self):
        extensions_names = ", ".join(extension.name for extension in self.extensions.all())
        if extensions_names:
            return f"{self.game.name} with extensions: {extensions_names}"
        else:
            return f"{self.game}"


class Play(models.Model):
    date = models.DateField(default=timezone.now)
    game_configuration = models.ForeignKey(GameConfiguration, on_delete=models.CASCADE, related_name='plays')
    players = models.ManyToManyField(settings.AUTH_USER_MODEL, through='PlayerScore', related_name='plays')

    def __str__(self):
        return f"{self.game_configuration} on {self.date}"


class PlayerScore(models.Model):
    play = models.ForeignKey(Play, on_delete=models.CASCADE)
    player = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.IntegerField()

    class Meta:
        unique_together = ('play', 'player')


class UserGameScore(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='game_scores')
    game_configuration = models.ForeignKey(GameConfiguration, on_delete=models.CASCADE, related_name='user_game_scores',
                                           null=True)
    total_score = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user', 'game_configuration')
