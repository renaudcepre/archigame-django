from django.contrib import admin

from .forms import PlayForm
from .models import Play, PlayerScore, Game, Extension


class ExtensionInline(admin.TabularInline):
    model = Extension
    extra = 0


class GameAdmin(admin.ModelAdmin):
    inlines = [ExtensionInline]


class PlayerScoreInline(admin.TabularInline):
    model = PlayerScore
    extra = 1  # Nombre de formulaires de score à afficher par défaut


class PlayAdmin(admin.ModelAdmin):
    inlines = [PlayerScoreInline]
    form = PlayForm
    list_display = ('date', 'game')


admin.site.register(Play, PlayAdmin)
admin.site.register(Game, GameAdmin)
