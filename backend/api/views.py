from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, permissions
from .serializers import UserSerializer, MovieSerializer, MovieDetailsSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from .models import Movie
import requests
from django.http import JsonResponse
from django.conf import settings
from rest_framework.views import APIView
import pandas as pd
from api.apps import MOVIE_SIMILARITY_DF
from django.views import View
from django.core.paginator import Paginator
from api.models import MovieDetails
from api.util import get_movie_details, get_movies_for_user
import json


RADARR_API_KEY = settings.RADARR_API_KEY
RADARR_URL = settings.RADARR_URL
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


class DeleteUserView(APIView):
    permission_classes = [permissions.AllowAny]  # Change this later for security

    def delete(self, request):
        username = request.data.get("username")  # Get username from request body
        if not username:
            return Response({"error": "username is required"}, status=400)

        user = User.objects.filter(username=username).first()
        if not user:
            return Response({"error": "User not found"}, status=404)

        user.delete()
        return Response({"message": "User deleted successfully"}, status=200)
    
@method_decorator(csrf_exempt, name='dispatch')
class AddMovieToRadarrView(View):
    def search_movie(self, title):
        """Search for a movie by title in Radarr"""
        url = f"{RADARR_URL}/api/v3/movie/lookup?term={title}"
        headers = {"X-Api-Key": RADARR_API_KEY}
        
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def add_movie(self, tmdb_id, root_folder="F:\Movies", quality_id=1):
        """Add a movie to Radarr using TMDB ID"""
        url = f"{RADARR_URL}/api/v3/movie"
        headers = {"X-Api-Key": RADARR_API_KEY, "Content-Type": "application/json"}
        
        payload = {
            "tmdbId": tmdb_id,
            "qualityProfileId": quality_id,
            "rootFolderPath": root_folder,
            "monitored": True,
            "addOptions": {"searchForMovie": True}
        }
        
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 201:
            return response.json()  # Successfully added
        else:
            return {"error": "Failed to add movie", "details": response.json()}

    @method_decorator(csrf_exempt)
    def post(self, request):
        """Handle POST request to search and add a movie"""
        try:
            data = json.loads(request.body)
            tmdb_id = data.get("tmdbId")
            if not tmdb_id:
                return JsonResponse({"error": "TMDB ID not found"}, status=400)
            add_response = self.add_movie(tmdb_id)
            return JsonResponse(add_response, status=200)
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)