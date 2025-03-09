from django.core.management.base import BaseCommand
from api.models import Movie

class Command(BaseCommand):
    help = "Deletes all movies from the database"

    def handle(self, *args, **kwargs):
        count, _ = Movie.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f"Deleted {count} movies from the database."))
