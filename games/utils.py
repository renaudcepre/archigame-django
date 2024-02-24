from django.db.models import Sum
from .models import PlayerScore, GameConfiguration
from users.models import User


def calculate_score(actual_score, min_score, max_score):
    score_range = max_score - min_score
    conversion_factor = 1000 / score_range

    if actual_score <= min_score:
        return 0

    return (actual_score - min_score) * conversion_factor


def calculate_total_score(user: User, game_configuration: GameConfiguration):
    # Calculer le score total directement dans la base de données
    total_score_aggregated = PlayerScore.objects.filter(
        player=user,
        play__game_configuration=game_configuration
    ).aggregate(total_score=Sum('score'))

    # total_score_aggregated['total_score'] pourrait être None si aucun score n'est trouvé
    total_score_from_db = total_score_aggregated.get('total_score') or 0


