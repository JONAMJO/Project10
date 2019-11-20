from django.db import models
from django.conf import settings


class Genre(models.Model):
    name = models.CharField(max_length=50)


class Movie(models.Model):
    title = models.CharField(max_length=50)
    audience = models.IntegerField()
    poster_url = models.CharField(max_length=200)
    description = models.TextField()
    genre = models.ManyToManyField(Genre)


class Review(models.Model):
    content = models.TextField()
    score = models.IntegerField()
    movie = models.ManyToManyField(Movie)
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    class Meta:
        ordering = ('-pk',)