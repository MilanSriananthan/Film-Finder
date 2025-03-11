import csv
from django.core.management.base import BaseCommand
from api.models import MovieIDs
import os
from django.conf import settings
import pandas as pd

class Command(BaseCommand):
    help = 'Imports movies from a CSV file into the database'

    def handle(self, *args, **kwargs):
        csv_path = os.path.join(settings.BASE_DIR, "links_cleaned.csv")
        if not os.path.exists(csv_path):
            self.stdout.write(self.style.ERROR(f"CSV file not found: {csv_path}"))
            return

        df = pd.read_csv(csv_path)

        # Clear the table (remove all existing records)
        MovieIDs.objects.all().delete()

        # Prepare list for bulk insert
        bulk_create_objs = []

        for _, row in df.iterrows():
            movie_id = row["movieId"]
            imdb_id = row["imdbId"]
            tmdb_id = row["tmdbId"]
            
            # Add the new record to the bulk insert list
            bulk_create_objs.append(MovieIDs(movie_id=movie_id, imdb_id=imdb_id, tmdb_id=tmdb_id))

        # Perform bulk insert
        if bulk_create_objs:
            MovieIDs.objects.bulk_create(bulk_create_objs)

        self.stdout.write(self.style.SUCCESS(f"Movie IDs imported successfully!"))
