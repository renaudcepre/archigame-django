from django.contrib import admin

from .forms import PlayForm, GameConfigurationForm
from .models import Play, PlayerScore, Game, Extension, GameConfiguration


class ExtensionInline(admin.TabularInline):
    model = Extension
    extra = 0


class GameAdmin(admin.ModelAdmin):
    inlines = [ExtensionInline]


class PlayerScoreInline(admin.TabularInline):
    model = PlayerScore
    extra = 1


class PlayAdmin(admin.ModelAdmin):
    inlines = [PlayerScoreInline]
    form = PlayForm
    list_display = ('date', 'game_configuration')


class GameConfigurationAdmin(admin.ModelAdmin):
    search_fields = ['game__name', 'extensions__name']
    filter_horizontal = ('extensions',)
    ordering = ('game__name',)

    form = GameConfigurationForm

    def display_extensions(self, obj):
        return len(obj.extensions.all())

    display_extensions.short_description = 'Extensions'


admin.site.register(GameConfiguration, GameConfigurationAdmin)

admin.site.register(Play, PlayAdmin)
admin.site.register(Game, GameAdmin)
