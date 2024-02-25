from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory

from .models import Game, Extension
from .models import GameConfiguration
from .models import Play


class PlayForm(forms.ModelForm):
    class Meta:
        model = Play
        fields = ['game_configuration', 'date']


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['name', 'bgg_number']


class ExtensionForm(forms.ModelForm):
    class Meta:
        model = Extension
        fields = ['name', 'bgg_number']


ExtensionFormSet = inlineformset_factory(Game, Extension, form=ExtensionForm, extra=1, can_delete=True)


class GameConfigurationForm(forms.ModelForm):
    class Meta:
        model = GameConfiguration
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        game = cleaned_data.get("game")
        extensions = cleaned_data.get("extensions", [])

        # Vérifie si chaque extension est liée au jeu spécifié.
        for extension in extensions:
            if extension.game != game:
                raise ValidationError(f"L'extension '{extension.name}' n'est pas liée au jeu '{game.name}'.")

        # Vérifie l'unicité de la combinaison jeu/extensions.
        if game:
            existing_configs = GameConfiguration.objects.filter(game=game)
            for config in existing_configs:
                # Convertit QuerySet en list pour comparaison, car 'extensions' est une liste à ce moment.
                if set(config.extensions.all()) == set(extensions):
                    raise ValidationError("Une configuration identique pour ce jeu existe déjà.")

        return cleaned_data
