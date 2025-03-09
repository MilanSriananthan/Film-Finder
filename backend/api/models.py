from django.db import models
from django.contrib.auth.models import User




class Movie(models.Model):
    PREFERENCE_CHOICES = [
        ('liked', 'Liked'),
        ('disliked', 'Disliked'),
        ('watch_later', 'Watch Later'),
        ('not_watched', 'Not Watched')
    ]

    id = models.IntegerField(primary_key=True)
    tmdb_id = models.IntegerField()
    title = models.CharField(max_length=100)
    adult = models.BooleanField()
    backdrop_path = models.CharField(max_length=100)
    genre_ids = models.JSONField()
    original_language = models.CharField(max_length=100)
    original_title = models.CharField(max_length=100)
    overview = models.TextField()
    popularity = models.FloatField()
    poster_path = models.CharField(max_length=100)
    release_date = models.DateField()
    video = models.BooleanField()
    vote_average = models.FloatField()
    vote_count = models.IntegerField()
    preferences = models.CharField(max_length=20, choices=PREFERENCE_CHOICES)

    def __str__(self):
        return self.title
    

class MovieIDs(models.Model):
    movie_id = models.IntegerField(primary_key=True)
    imdb_id = models.CharField(max_length=100)
    tmdb_id = models.IntegerField()

    def __str__(self):
        return f"Movie {self.movie_id} - {self.imdb_id} - {self.tmdb_id}"