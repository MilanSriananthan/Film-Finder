from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer, MovieSerializer, MovieDetailsSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Movie
import requests
from django.http import JsonResponse
from django.conf import settings
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
import pandas as pd
from api.apps import MOVIE_SIMILARITY_DF
from django.views import View
from django.core.paginator import Paginator
from api.models import MovieDetails
from api.util import get_movie_details, get_movies_for_user
import random


TMDB_API_KEY = settings.TMDB_API_KEY

def get_top_rated_movies(request):
    page = request.GET.get('page', 1)
    url = f"https://api.themoviedb.org/3/movie/top_rated?language=en-US&page={page}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TMDB_API_KEY}",
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return JsonResponse(data["results"], safe=False)
    else:
        return JsonResponse({"error": "Failed to fetch data"})
    
    
def recommend_movies(user):
    """
    Recommend movies for a new user based on their ratings.
    :param new_user_ratings: Dict {item_id: rating} for the new user
    :param top_n: Number of recommendations to return
    :return: List of recommended movie titles
    """
    top_n = 10

    preference_to_rating = {
        'liked': 5.0,
        'disliked': 1.0,
        'watch_later': 3.0,
        'not_watched': 0.0  # This won't be considered for recommendations
    }

    user_movies = Movie.objects.filter(user=user)
    new_user_ratings = {}
    for movie in user_movies:
        if movie.preferences in preference_to_rating:
            rating = preference_to_rating[movie.preferences]
            new_user_ratings[movie.movie_details_id] = rating
            
    similar_scores = pd.Series(dtype=float)

    for item_id, rating in new_user_ratings.items():
        if item_id in MOVIE_SIMILARITY_DF.index:
            similar_movies = MOVIE_SIMILARITY_DF[item_id] * rating
            similar_movies = similar_movies.sort_values(ascending=False)

            similar_scores = similar_scores.add(similar_movies, fill_value=0)

    similar_scores = similar_scores.drop(index=new_user_ratings.keys(), errors="ignore")

    recommended_movie_ids = similar_scores.sort_values(ascending=False).head(top_n).index.tolist()

    return recommended_movie_ids

class MovieListCreate(generics.ListCreateAPIView):
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        preference = self.request.query_params.get("preference", None)
        movies = get_movies_for_user(user, preference)
        return movies
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class MovieDetailsList(generics.ListAPIView):  # Read-only view for listing movies
    serializer_class = MovieDetailsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        preference = self.request.query_params.get("preference", None)

        # Get movies filtered by user and preference, returning only their details
        return MovieDetails.objects.filter(
            movie_id__in=Movie.objects.filter(user=user, preferences=preference)
            .values_list('movie_details', flat=True))

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class MovieListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = self.request.user
        watched_movies = Movie.objects.filter(user=user)
        unwatched_movies = list(MovieDetails.objects.exclude(movie_id__in=watched_movies.values('movie_details')).values_list('movie_id', flat=True)[:10])
        recommended_movie_ids = recommend_movies(user)
        filtered_recommended_movie_ids = list(set(unwatched_movies + recommended_movie_ids))
        recommended_movie_details = MovieDetails.objects.filter(movie_id__in=filtered_recommended_movie_ids).values(
            'movie_id', 'imdb_id', 'tmdb_id', 'title', 'adult', 'backdrop_path', 'genre_ids', 
            'original_language', 'original_title', 'overview', 'popularity', 'poster_path', 
            'release_date', 'video', 'vote_average', 'vote_count'
        )

        return JsonResponse({
            "movies": list(recommended_movie_details)
        })
