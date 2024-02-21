from django import forms
from django.core.exceptions import ValidationError
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
