from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Movie


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(**validated_data)
        return user




class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ["id", "tmdb_id", "title", "adult", "backdrop_path", "genre_ids", "original_language", "original_title", "overview", "popularity", "poster_path", "release_date", "video", "vote_average", "vote_count", "preferences"]

    def create(self, validated_data):
        movie, created = Movie.objects.update_or_create(
            id=validated_data["id"], defaults=validated_data
        )
        return movie
