from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


class UserAdmin(BaseUserAdmin):
    list_display = BaseUserAdmin.list_display + ('total_score_display', 'total_games_display',)

    def total_score_display(self, obj):
        return obj.total_score()

    total_score_display.short_description = 'Total Score'

    def total_games_display(self, obj):
        return obj.total_plays()

    total_games_display.short_description = 'Total Games'


admin.site.register(User, UserAdmin)
