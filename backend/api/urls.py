from django.urls import path
from . import views

urlpatterns = [
    path("movies/", views.MovieListCreate.as_view(), name="movie-list"),
    path("movies/details/", views.MovieDetailsList.as_view(), name="movie-details"),
    path("movies/top-rated/", views.get_top_rated_movies, name="top-rated-movies"),
    path("movies/watch-later/", views.MovieListCreate.as_view(), name="watch-later-movies"),
    path("movies/recommendations/", views.recommend_movies, name="recomendations-movies"),
    path("movies-details/", views.MovieListView.as_view(), name="movie-list"),
    path("add-movie/", views.AddMovieToRadarrView.as_view(), name="add_movie"),
    path("movies/all/", views.MovieDetailsAll.as_view(), name="movie-list"),
]