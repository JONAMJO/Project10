from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Movie, Genre, Review
from .forms import ReviewForm


# Create your views here.

def index(request):
    movies = Movie.objects.all()
    context = {'movies': movies}
    return render(request, 'movies/index.html', context)


def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    reviews = movie.review_set.all()
    person = get_object_or_404(get_user_model(), pk=movie.user_id)
    review_form = ReviewForm()
    context = {
        'movie': movie,
        'review_form': review_form,
        'reviews': reviews,
        'person': person,
    }
    return render(request, 'movies/detail.html', context)

  
@require_POST
def reviews_create(request, movie_pk):
    review_form = ReviewForm(request.POST)
    if review_form.is_valid():
        review = review_form.save(commit=False)
        review.movie_id = movie_pk
        review.save()
    return redirect('movies:detail', movie_pk)

