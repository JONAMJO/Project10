from django import forms
from .models import Movie, Review


class MovieForm(forms.ModelForm):
    title = forms.CharField(label='영화명', max_length=10)
    title_en = forms.CharField(label='영화명(영문)', max_length=10)
    audience = forms.IntegerField(label='누적 관객수')
    open_date = forms.DateField(label='개봉일')
    genre = forms.CharField(label='장르', max_length=10)
    watch_grade = forms.CharField(label='관람등급', max_length=10)
    score = forms.FloatField(label='평점')
    poster_url = forms.CharField(label='포스터 이미지 URL', max_length=10)
    description = forms.Textarea()


    class Meta:
      model = Movie
      fields = '__all__'


class ReviewForm(forms.ModelForm):

    class Meta:
      model = Review
      fields = ('content', 'score')
