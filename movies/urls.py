from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:movie_pk>/', views.detail, name='detail'),
    path('<int:movie_pk>/reviews_create', views.reviews_create, name='reviews_create'),
    path('<int:movie_pk>/reviews_delete/<int:review_pk>', views.reviews_delete, name='reviews_delete'),
    path('<int:movie_pk>/like/', views.like, name='like')
]
