from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from games.models import PlayerScore, UserGameScore


def calculate_score(actual_score, min_score, max_score):
    score_range = max_score - min_score
    conversion_factor = 1000 / score_range

    if actual_score <= min_score:
        return 0

    return (actual_score - min_score) * conversion_factor


@receiver(post_save, sender=PlayerScore)
def update_user_game_score(sender, instance, created, **kwargs):
    if created:
        game_configuration = instance.play.game_configuration
        user_game_score, created = UserGameScore.objects.get_or_create(
            user=instance.player,
            game_configuration=game_configuration
        )

        user_game_score.total_score += calculate_score(instance.score, game_configuration.score_min,
                                                       game_configuration.score_max)
        user_game_score.save()


@receiver(pre_delete, sender=PlayerScore)
def adjust_user_game_scores_on_play_deletion(sender, instance, **kwargs):
    game_configuration = instance.play.game_configuration
    user_game_score, created = UserGameScore.objects.get_or_create(
        user=instance.player,
        game_configuration=game_configuration
    )
    points_to_subtract = calculate_score(instance.score,
                                         instance.play.game_configuration.score_min,
                                         instance.game_configuration.game.score_max)
    user_game_score.total_score = max(user_game_score.total_score - points_to_subtract, 0)
    user_game_score.save()
