from django.db import models
from django.conf import settings

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=100)


class Movie(models.Model):
    adult = models.BooleanField()
    backdrop_path = models.CharField(max_length=500, null=True)
    genres = models.ManyToManyField(Genre, related_name='movie_genre')
    original_language = models.CharField(max_length=20)
    original_title = models.CharField(max_length=200)
    overview = models.TextField(null=True)
    popularity = models.FloatField(null=True)
    poster_path = models.CharField(max_length=500, null=True)
    release_date = models.DateField(null=True)
    title = models.CharField(max_length=200)
    vote_average = models.FloatField(null=True)
    vote_count = models.IntegerField(null=True)
    vote_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="vote_movie", blank=True)
    

class Review(models.Model):
    title = models.CharField(max_length=100)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    

class Comment(models.Model):
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)

class Rate(models.Model):
    rank = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

