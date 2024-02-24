import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'archigame.settings')
django.setup()

from users.models import User
from games.models import Game, Extension, GameConfiguration, Play, PlayerScore


# Crée des utilisateurs
def create_users(n):
    for i in range(n):
        username = f'user{i}'
        email = f'user{i}@example.com'
        user = User.objects.create_user(username=username, email=email, password='testpassword')
        print(f'User created: {user.username}')


# Crée des jeux et des extensions
def create_games_and_extensions(n):
    for i in range(n):
        game = Game.objects.create(name=f'Game{i}', bgg_number=i)
        for j in range(random.randint(1, 3)):  # Chaque jeu aura de 1 à 3 extensions
            Extension.objects.create(game=game, name=f'Extension{j} of Game{i}')
        print(f'Game created: {game.name} with {j + 1} extensions')


# Crée des configurations de jeu
def create_game_configurations():
    for game in Game.objects.all():
        GameConfiguration.objects.create(
            game=game,
            min_players=random.randint(1, 2),
            max_players=random.randint(3, 5),
            score_min=0,
            score_max=100
        )
        print(f'GameConfiguration created for {game.name}')


# Crée des parties et des scores de joueurs
def create_plays_and_scores():
    users = list(User.objects.all())
    game_configurations = GameConfiguration.objects.all()
    for gc in game_configurations:
        play = Play.objects.create(date=django.utils.timezone.now(), game_configuration=gc)
        for user in random.sample(users, k=random.randint(1,
                                                          gc.max_players)):  # Sélectionne aléatoirement entre 1 et max_players utilisateurs
            PlayerScore.objects.create(play=play, player=user, score=random.randint(0, 100))
        print(f'Play created for {gc.game.name} on {play.date} with {len(users)} players')


def main():
    # create_users(5)
    # create_games_and_extensions(3)
    # create_game_configurations()
    create_plays_and_scores()


if __name__ == '__main__':
    main()
