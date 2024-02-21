from django.conf import settings
from django.db import models
from django.utils import timezone


class Game(models.Model):
    name = models.CharField(max_length=255)
    bgg_number = models.IntegerField(null=True)

    def __str__(self):
        return self.name


class Extension(models.Model):
    game = models.ForeignKey(Game, related_name='extensions', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    bgg_number = models.IntegerField(null=True)

    def __str__(self):
        return self.name


class Play(models.Model):
    date = models.DateField(default=timezone.now)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    extensions = models.ManyToManyField(Extension, blank=True)
    players = models.ManyToManyField(settings.AUTH_USER_MODEL, through='PlayerScore', related_name='plays')

    def __str__(self):
        return f"{self.game.name} on {self.date}"


class PlayerScore(models.Model):
    play = models.ForeignKey(Play, on_delete=models.CASCADE)
    player = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.IntegerField()

    class Meta:
        unique_together = ('play', 'player')
