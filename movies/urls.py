from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:movie_pk>/', views.detail, name='detail'),
    path('<int:movie_pk>/delete/', views.delete, name='delete'),
    path('<int:movie_pk>/update/', views.update, name='update'),
    path('<int:movie_pk>/comments/', views.comments_create, name='comments_create'),
    path(
        '<int:movie_pk>/comments/<int:comment_pk>/delete/',
        views.comments_delete,
        name='comments_delete',
    ),
    path('<int:movie_pk>/like/', views.like, name='like'),
    path('<int:movie_pk>/follow/<int:user_pk>/', views.follow, name='follow'),
    path('<int:hash_pk>/hashtag/', views.hashtag, name='hashtag'),
]
