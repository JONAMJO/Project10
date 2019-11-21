from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Movie, Genre, Review
from .forms import ReviewForm

# Create your views here.

def index(request):
    movie = Movie.objects.all()
    context = {'movie': movie}
    return render(request, 'movies/index.html', context)


def detail(request, movie_pk):
    movie = get_object_or_404(Article, pk=movie_pk)
    reviews = movie.review_set.all()
    person = get_object_or_404(get_user_model(), pk=movie.user_id)
    context = {
        'movie': movie,
        'review_form': review_form,
        'reviews': reviews,
        'person': person,
    }
    return render(request, 'movies/detail.html', context)

