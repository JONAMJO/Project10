## PJT10 - Django (Pair Programming)

### :one: 목표

- 협업을 통한 데이터베이스 모델링 및 기능 구현



### :two: 준비 사항

1. (필수) Python Web Framework
   - Django 2.2.7
   - Python 3.7.3

2. (선택) 샘플 영화 정보
3. (선택) Github Flow



### :three: 데이터베이스 모델링

- 테이블 간의 관계를 파악하여 작성하였다.

- Seed Data 구성
  - 임의의 데이터를 직접 추가 해보고 fixture 파일을 생성하였다.



### :four:  업무분담

- 남승현 : 데이터베이스 모델링, movies App
- 조현호 : movies/detail, accounts App
  

### :five:`accounts` App

```python
# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

admin.site.register(User, UserAdmin)
```

```python
# models.py
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followings')
```

```python
# forms.py
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ('email',)
```

```python
# urls.py
from django.urls import path
from . import views

app_name='accounts'
urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('<int:user_pk>/', views.profile, name='profile'),
]
```

```python
# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib.auth import get_user_model
from .models import User


def index(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'accounts/index.html', context)


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
        return redirect('movies:index')
    else:
        form = CustomUserCreationForm()
    context = {'form': form}
    return render(request, 'accounts/signup.html', context)


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
        return redirect(request.GET.get('next') or 'movies:index')
    else:
        form = AuthenticationForm()
    context = {'form': form}
    return render(request, 'accounts/login.html', context)


@login_required
def logout(request):
    auth_logout(request)
    return redirect('movies:index')


@login_required
def profile(request, user_pk):
    profile_user = get_object_or_404(User, pk=user_pk)
    context = {'profile_user': profile_user}
    return render(request, 'accounts/profile.html', context)
```



### :six: `movies` App

```python
# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Userfrom django.contrib import admin
from .models import Genre, Movie, Review

class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(Genre, GenreAdmin)


class MovieAdmin(admin.ModelAdmin):
    list_display = ('title',)
admin.site.register(Movie, MovieAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('content', 'score', 'movie', 'user')
admin.site.register(Review, ReviewAdmin)

admin.site.register(User, UserAdmin)
```

```python
# models.py
from django.db import models
from django.conf import settings


class Genre(models.Model):
    name = models.CharField(max_length=20)


class Movie(models.Model):
    title = models.CharField(max_length=30)
    audience = models.IntegerField()
    poster_url = models.CharField(max_length=140)
    description = models.TextField()
    genres = models.ManyToManyField(Genre, related_name='movies')
    liked_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_movies', blank=True)


class Review(models.Model):
    content = models.CharField(max_length=140)
    score = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
```

```python
# forms.py
from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('content', 'score',)
```

```python
# urls.py
from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:movie_pk>/', views.detail, name='detail'),
    path('<int:movie_pk>/reviews/create/', views.review_create, name='review_create'),
    path('<int:movie_pk>/reviews/<int:review_pk>/delete/', views.review_delete, name='review_delete'),
    path('<int:movie_pk>/like/', views.like, name='like'),
]
```

```python
# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Movie, Genre, Review
from .forms import ReviewForm


@require_GET
def index(request):
    movies = Movie.objects.all()
    context = {'movies': movies}
    return render(request, 'movies/index.html', context)


@require_GET
def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    review_form = ReviewForm()
    # person = get_object_or_404(get_user_model(), pk=movie.user_id)
    reviews = movie.reviews.all()
    context = {'movie': movie, 'review_form': review_form, 'reviews': reviews}
    return render(request, 'movies/detail.html', context)


@require_POST
def review_create(request, movie_pk):
    if request.user.is_authenticated:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie_id = movie_pk
            review.user = request.user
            review.save()
            return redirect('movies:detail', movie_pk)
    return redirect('movies:index')


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

```



### :seven: 회고록

- 남승현: 

  ```
  1. model 생성 시 manytomany Field 사용하는 것이 익숙하지 않았다.
  2. 댓글삭제 구현 시 csrf를 추가하지 않은 실수를 했다.
  3. 다른 팀원과 코드를 merge할 경우 곂치는 부분을 수정하는 것이 힘들었다.
  4. 팀원과의 원만한 소통을 통해 프로젝트를 완성할 수 있었다.
  ```

- 조현호:

  ```
  1. 좋아요 기능 구현시 아이콘이 화면에 나오지 않았는데 키를 추가하지 않았었다.
  2. 유저 프로필 페이지에 리뷰 목록을 나타내는데 변수명을 잘 못 지정해서 수정을 하였다.
  3. 팀원과 github에서 코드를 merge 하는 것이 익숙하지 않아 힘들었다.
  ```

  

### :eight: 결과

1. Movies index 페이지

   ![캡처1](https://user-images.githubusercontent.com/52685280/69308345-de13d900-0c6e-11ea-82eb-ec194f7e73f9.PNG)

   <hr>

2. Movies detail 페이지

   ![캡처2](https://user-images.githubusercontent.com/52685280/69308378-dfdd9c80-0c6e-11ea-8171-340529f25379.PNG)

   <hr>

3. Accounts index 페이지

   ![캡처3](https://user-images.githubusercontent.com/52685280/69308404-e23ff680-0c6e-11ea-82df-3d2e0d1d22c2.PNG)

   <hr>

4. Accounts profile 페이지

   ![캡처4](https://user-images.githubusercontent.com/52685280/69308427-e409ba00-0c6e-11ea-9012-239ff8a446f7.PNG)

