from django.shortcuts import render, get_object_or_404
from .models import Movie

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