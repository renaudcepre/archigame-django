from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import Sum
from .models import User, UserGameScore

# Définition d'une nouvelle classe d'admin pour User
class UserAdmin(BaseUserAdmin):
    def total_score(self, obj):
        return UserGameScore.objects.filter(user=obj).aggregate(total=Sum('total_score'))['total'] or 0

    total_score.short_description = 'Total Score'  #

    list_display = BaseUserAdmin.list_display + ('total_score',)


admin.site.register(User, UserAdmin)
