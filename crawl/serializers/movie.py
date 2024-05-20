from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from crawl.models import Movie, MoviePhoto, MovieSimilarity


class MoviePhotoSerializer(ModelSerializer):

    class Meta:
        model = MoviePhoto
        fields = [
            "file",
            "downloaded_url",
            "photo_code",
        ]


class SimilarMoviesSerializer(ModelSerializer):
    code = serializers.CharField(source='is_similar_to.code', read_only=True)

    class Meta:
        model = MovieSimilarity
        fields = [
            "is_similar_to",
            "code",
        ]


class MovieSerializer(ModelSerializer):
    code = serializers.CharField(source="movie_code.code", read_only=True)
    photos = MoviePhotoSerializer(many=True, read_only=True)
    more_like_this = serializers.SerializerMethodField()

    def get_more_like_this(self, instance: Movie):
        serializer = SimilarMoviesSerializer(
            instance=MovieSimilarity.objects.filter(the_case=instance.movie_code), many=True
        )
        return serializer.data

    class Meta:
        model = Movie
        fields = [
            "code",
            "title",
            "story_line",
            "rating_value",
            "rating_count",
            "photos",
            "more_like_this",
        ]
