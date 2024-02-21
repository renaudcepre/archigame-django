from django.db import models

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
