from django.db import models
from django.contrib.auth.models import User


class MovieDetails(models.Model):
    movie_id = models.IntegerField(primary_key=True)
    imdb_id = models.CharField(max_length=20, unique=True)  # IMDB ID length adjustment
    tmdb_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    adult = models.BooleanField(default=False)
    backdrop_path = models.CharField(max_length=255, null=True, blank=True)
    genre_ids = models.JSONField()
    original_language = models.CharField(max_length=10)  # Typically a short ISO code
    original_title = models.CharField(max_length=255)
    overview = models.TextField(null=True, blank=True)
    popularity = models.FloatField(default=0.0)
    poster_path = models.CharField(max_length=255, null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)  # Allow null and blank
    video = models.BooleanField(default=False)
    vote_average = models.FloatField(default=0.0)
    vote_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title} (TMDB: {self.tmdb_id})"

class Movie(models.Model):
    PREFERENCE_CHOICES = [
        ('liked', 'Liked'),
        ('disliked', 'Disliked'),
        ('watch_later', 'Watch Later'),
        ('not_watched', 'Not Watched')
    ]
    
    preferences = models.CharField(max_length=20, choices=PREFERENCE_CHOICES)
    user = models.ForeignKey(User, related_name='movies', on_delete=models.CASCADE)
    movie_details = models.ForeignKey(MovieDetails, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        unique_together = ('movie_details', 'user')  # Prevents duplicate preferences for the same user and movie

    def __str__(self):
        return f"Movie {self.movie_details} - {self.preferences} ({self.user.username})"
    

