from dataclasses import dataclass
import requests
from datetime import datetime
from django.conf import settings
from .models import Movie, MovieDetails

TMDB_API_KEY = settings.TMDB_API_KEY
@dataclass
class MovieDetailsData:
    title: str
    adult: bool
    backdrop_path: str
    genre_ids: list[int]
    original_language: str
    original_title: str
    overview: str
    popularity: float
    poster_path: str
    release_date: str  # Keeping it as a string in 'YYYY-MM-DD' format
    video: bool
    vote_average: float
    vote_count: int

def get_movie_details(tmdb_id):
    """
    Fetch movie details from TMDB API based on tmdb_id and return a structured object.
    :param tmdb_id: TMDB movie ID.
    :return: MovieDetails object or None if request fails.
    """
    url = f'https://api.themoviedb.org/3/movie/{tmdb_id}'
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TMDB_API_KEY}",
    }
    
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()

        return MovieDetailsData(
            title=data.get("title", ""),
            adult=data.get("adult", False),
            backdrop_path=data.get("backdrop_path", ""),
            genre_ids=[genre["id"] for genre in data.get("genres", [])],
            original_language=data.get("original_language", ""),
            original_title=data.get("original_title", ""),
            overview=data.get("overview", ""),
            popularity=data.get("popularity", 0.0),
            poster_path=data.get("poster_path", ""),
            release_date=data.get("release_date", ""),
            video=data.get("video", False),
            vote_average=data.get("vote_average", 0.0),
            vote_count=data.get("vote_count", 0),
        )
    
    return None


def get_movies_for_user(user, preference=None):
    # Get movies for the user based on preference
    movies = Movie.objects.filter(user=user)
    if preference:
        movies = movies.filter(preferences=preference)

    return movies