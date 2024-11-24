from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')
    search_fields = ('user__username', 'bio')
    filter_horizontal = ('watchlist', 'favorites')  # Optimized UI for ManyToManyFields
