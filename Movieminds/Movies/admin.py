from django.contrib import admin
from .models import Category, Actor, Movie, Rating, Comment

# Admin for Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('name',)

# Admin for Actor
@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_of_birth')
    search_fields = ('name', 'biography')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('date_of_birth',)

# Admin for Movie
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'posted_by', 'release_date', 'average_rating', 'created', 'updated')
    search_fields = ('title', 'description')
    list_filter = ('release_date', 'category')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('actors',)  # For ManyToManyField
    readonly_fields = ('average_rating',)

# Admin for Rating
@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('movie', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('movie__title', 'user__username')

# Admin for Comment
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('movie', 'user', 'content', 'parent', 'created_at', 'updated_at')
    search_fields = ('movie__title', 'user__username', 'content')
    list_filter = ('created_at', 'updated_at')
    raw_id_fields = ('parent',)  # For quick navigation to parent comments
