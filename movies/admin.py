from django.contrib import admin
from .models import Genre, Movie, Review

# Register your models here.
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(Genre, GenreAdmin)


class MovieAdmin(admin.ModelAdmin):
    list_display = ('title',)
admin.site.register(Movie, MovieAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('content', 'score', 'movie', 'user')
admin.site.register(Review, ReviewAdmin)
