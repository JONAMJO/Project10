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
    reviews = movie.reviews.all()
    context = {'movie': movie, 'review_form': review_form, 'reviews': reviews}
    return render(request, 'movies/detail.html', context)


@ login_required
def reviews_create(request, movie_pk):
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.movie_id = movie_pk
            review.user_id = request.user.pk
            review.save()
    return redirect('movies:detail', movie_pk)

  
@require_POST
def review_delete(request, movie_pk, review_pk):
    if request.user.is_authenticated:
        review = get_object_or_404(Review, pk=review_pk)
        if review.user == request.user:
            review.delete()
        return redirect('movies:detail', movie_pk)
    return HttpResponse('You are Unauthorized', status=401)


def like(request, movie_pk):
    user = request.user
    movie = get_object_or_404(Movie, pk=movie_pk)
    if user in movie.liked_users.all():
        user.liked_movies.remove(movie)
    else:
        user.liked_movies.add(movie)
    return redirect('movies:detail', movie_pk)
