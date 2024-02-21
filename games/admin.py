from django.contrib import admin

from .models import Game, Extension


class ExtensionInline(admin.TabularInline):
    model = Extension
    extra = 0


class GameAdmin(admin.ModelAdmin):
    inlines = [ExtensionInline]


admin.site.register(Game, GameAdmin)

