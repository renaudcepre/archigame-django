from django import forms
from django.core.exceptions import ValidationError

from .models import Game
from .models import GameConfiguration
from .models import Play


class PlayForm(forms.ModelForm):
    class Meta:
        model = Play
        fields = ['game', 'extensions', 'players', 'date']

    def clean(self):
        cleaned_data = super().clean()
        game = cleaned_data.get("game")
        extensions = cleaned_data.get("extensions")

        if extensions and game:
            for extension in extensions:
                if extension.game != game:
                    raise ValidationError("Toutes les extensions doivent appartenir au jeu sélectionné.")

        return cleaned_data


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['name', 'bgg_number']


class GameConfigurationForm(forms.ModelForm):
    class Meta:
        model = GameConfiguration
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        game = cleaned_data.get("game")
        extensions = cleaned_data.get("extensions")

        for extension in extensions:
            if extension.game != game:
                raise ValidationError(f"L'extension '{extension.name}' n'est pas liée au jeu '{game.name}'.")

        return cleaned_data
