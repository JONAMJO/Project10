from django.contrib import admin
from .models import Genre, Movie, Review

# Register your models here.

class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)


class MovieAdmin(admin.ModelAdmin):
    list_display = ('title',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('content',)



admin.site.register(Genre, GenreAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Review, ReviewAdmin)