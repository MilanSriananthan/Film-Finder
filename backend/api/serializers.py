from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Movie, MovieDetails


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(**validated_data)
        return user


class MovieDetailsSerializer(serializers.ModelSerializer):
    """Serializer for returning only movie details."""
    
    class Meta:
        model = MovieDetails
        fields = "__all__"  # Include all fields of MovieDetails

class MovieSerializer(serializers.ModelSerializer):
    movie_details = serializers.PrimaryKeyRelatedField(queryset=MovieDetails.objects.all())

    class Meta:
        model = Movie
        fields = ['preferences', 'movie_details']  # user is handled in the view
        read_only_fields = ['user']  # Make user read-only as it's set automatically

    def validate_movie_details(self, value):
        """
        Custom validation to check if the MovieDetails object exists.
        """
        if not MovieDetails.objects.filter(movie_id=value.movie_id).exists():
            raise serializers.ValidationError("Movie details not found for the provided movie_id.")
        return value
    
