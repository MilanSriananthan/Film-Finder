from django.apps import AppConfig
import pandas as pd
from django.conf import settings
import os

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        """Load the precomputed similarity matrix when Django starts."""
        similarity_path = os.path.join(settings.BASE_DIR, "movie_similarity.parquet")

        try:
            # Load the matrix into a global variable
            global MOVIE_SIMILARITY_DF
            MOVIE_SIMILARITY_DF = pd.read_parquet(similarity_path)
            print("✅ Loaded movie similarity matrix successfully!")
        except Exception as e:
            print(f"⚠️ Error loading movie similarity matrix: {e}")
