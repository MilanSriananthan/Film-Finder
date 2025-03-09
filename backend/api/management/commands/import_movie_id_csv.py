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
        
        for _, row in df.iterrows():
            MovieIDs.objects.update_or_create(
                movie_id=row["movieId"],
                defaults={
                    "imdb_id": row["imdbId"],
                    "tmdb_id": row["tmdbId"]
                },
            )

        self.stdout.write(self.style.SUCCESS("Movie IDs imported successfully!"))