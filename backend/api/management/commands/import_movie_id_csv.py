import csv
from django.core.management.base import BaseCommand
from api.models import MovieDetails
import os
from django.conf import settings
import pandas as pd
from api.util import get_movie_details

class Command(BaseCommand):
    help = 'Imports movies from a CSV file into the database'

    def handle(self, *args, **kwargs):
        csv_path = os.path.join(settings.BASE_DIR, "links_cleaned_copy.csv")
        if not os.path.exists(csv_path):
            self.stdout.write(self.style.ERROR(f"CSV file not found: {csv_path}"))
            return

        df = pd.read_csv(csv_path)

        # Clear the table (remove all existing records)
        MovieDetails.objects.all().delete()

        # Prepare list for bulk insert
        bulk_create_objs = []

        for _, row in df.iterrows():
            movie_id = row["movieId"]
            imdb_id = row["imdbId"]
            tmdb_id = int(row["tmdbId"])
            movie_data = get_movie_details(tmdb_id)
            if movie_data:  # Ensure data retrieval was successful
                bulk_create_objs.append(
                    MovieDetails(
                        movie_id=movie_id,
                        imdb_id=imdb_id,
                        tmdb_id=tmdb_id,
                        title=movie_data.title,
                        adult=movie_data.adult,
                        backdrop_path=movie_data.backdrop_path,
                        genre_ids=movie_data.genre_ids,
                        original_language=movie_data.original_language,
                        original_title=movie_data.original_title,
                        overview=movie_data.overview,
                        popularity=movie_data.popularity,
                        poster_path=movie_data.poster_path,
                        release_date=movie_data.release_date,
                        video=movie_data.video,
                        vote_average=movie_data.vote_average,
                        vote_count=movie_data.vote_count,
                    )
                )
            else:
                self.stdout.write(self.style.WARNING(f"Skipping movie ID {movie_id}: Data not found."))

        # Perform bulk insert
        if bulk_create_objs:
            MovieDetails.objects.bulk_create(bulk_create_objs)

        self.stdout.write(self.style.SUCCESS("Movie IDs imported successfully!"))