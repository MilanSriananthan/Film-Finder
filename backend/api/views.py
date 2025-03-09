from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer, MovieSerializer
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
from api.models import MovieIDs
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
    
def get_movie_details(request, tmdb_id):
    """
    Fetch movie details from TMDB API based on tmdb_id.
    :param tmdb_id: TMDB movie ID.
    :return: JSON response with movie details.
    """
    # Define the TMDB API URL for movie details
    url = f'https://api.themoviedb.org/3/movie/{tmdb_id}'
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TMDB_API_KEY}",
    }
    # Send a GET request to the TMDB API
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        # Parse the response from TMDB
        data = response.json()
        
        # Extract relevant information from the response
        movie_details = {
            'title': data.get('title', 'No title available'),
            'description': data.get('overview', 'No description available'),
            'backdrop_path': f'https://image.tmdb.org/t/p/w500{data.get("backdrop_path", "")}',
        }
        
        return JsonResponse({'error':data}, status=200)
    
    else:
        # If the request to TMDB fails, return an error message
        return JsonResponse({'error': 'Failed to retrieve movie details from TMDB'}, status=400)
    
def recommend_movies(request):
    """
    Recommend movies for a new user based on their ratings.
    :param new_user_ratings: Dict {item_id: rating} for the new user
    :param top_n: Number of recommendations to return
    :return: List of recommended movie titles
    """
    top_n = 10

    user = request.user

    preference_to_rating = {
        'liked': 5.0,
        'disliked': 1.0,
        'watch_later': 3.0,
        'not_watched': 0.0  # This won't be considered for recommendations
    }

    user_movies = Movie.objects.all()
    new_user_ratings = {}
    for movie in user_movies:
        if movie.preferences in preference_to_rating:
            rating = preference_to_rating[movie.preferences]
            new_user_ratings[movie.id] = rating
            
    similar_scores = pd.Series(dtype=float)

    for item_id, rating in new_user_ratings.items():
        if item_id in MOVIE_SIMILARITY_DF.index:
            # Multiply similarity score by the user's rating
            similar_movies = MOVIE_SIMILARITY_DF[item_id] * rating
            similar_movies = similar_movies.sort_values(ascending=False)

            # Accumulate scores
            similar_scores = similar_scores.add(similar_movies, fill_value=0)

    # Remove already seen movies
    similar_scores = similar_scores.drop(index=new_user_ratings.keys(), errors="ignore")

    # Get top N recommended movie IDs
    recommended_movie_ids = similar_scores.sort_values(ascending=False).head(top_n).index.tolist()

    # Convert item IDs to movie titles
    #recommended_movies = [movie_titles.get(movie_id, f"Movie {movie_id}") for movie_id in recommended_movie_ids]

    return recommended_movie_ids

class MovieListCreate(generics.ListCreateAPIView):
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        preference = self.request.query_params.get("preference", None)

        if preference:
            return Movie.objects.filter(preferences=preference)
        
        return Movie.objects.all()
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class MovieListView(View):
    def get(self, request):
        page = int(request.GET.get("page", 1))  # Default to page 1
        movies = MovieIDs.objects.all()
        
        recommended_movie_ids = recommend_movies(request)

        paginator = Paginator(movies, 10)  # Show 10 movies per page
        movie_page = paginator.get_page(page)

        movie_data = []
        for movie in movie_page:

            url = f'https://api.themoviedb.org/3/movie/{movie.tmdb_id}'
            headers = {
                "accept": "application/json",
                "Authorization": f"Bearer {TMDB_API_KEY}",
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                movie_data.append({
                    "id": movie.movie_id,
                    "tmdb_id": movie.tmdb_id,
                    "title": data.get("title"),
                    "overview": data.get("overview"),
                    "poster_path": data.get("poster_path"),
                    "backdrop_path": data.get("backdrop_path"),
                    "release_date": data.get("release_date"),
                    "adult": data.get("adult"),
                    "genre_ids": data.get("genres", []),  # Default to empty list if not available
                    "original_language": data.get("original_language"),
                    "original_title": data.get("original_title"),
                    "popularity": data.get("popularity"),
                    "video": data.get("video"),
                    "vote_average": data.get("vote_average"),
                    "vote_count": data.get("vote_count"),
                })
        
        random_movies = random.sample(movie_data, min(5, len(movie_data)))

        recommended_movie_data = []
        for movie_id in recommended_movie_ids:
            # Fetch the TMDB details for the recommended movies
            movie = MovieIDs.objects.filter(movie_id=movie_id).first()
            if movie:
                url = f'https://api.themoviedb.org/3/movie/{movie.tmdb_id}'
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    recommended_movie_data.append({
                        "id": movie.movie_id,
                        "tmdb_id": movie.tmdb_id,
                        "title": data.get("title"),
                        "overview": data.get("overview"),
                        "poster_path": data.get("poster_path"),
                        "backdrop_path": data.get("backdrop_path"),
                        "release_date": data.get("release_date"),
                        "adult": data.get("adult"),
                        "genre_ids": data.get("genres", []),
                        "original_language": data.get("original_language"),
                        "original_title": data.get("original_title"),
                        "popularity": data.get("popularity"),
                        "video": data.get("video"),
                        "vote_average": data.get("vote_average"),
                        "vote_count": data.get("vote_count"),
                    })

        # Combine random movies and recommended movies
        combined_movie_data = recommended_movie_data + random_movies

        return JsonResponse({
            "movies": combined_movie_data,
            "page": movie_page.number,
            "total_pages": paginator.num_pages,
        })
