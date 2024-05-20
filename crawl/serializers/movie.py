
from rest_framework import serializers 
from rest_framework.serializers import ModelSerializer

from crawl.models import Movie, MoviePhoto


class MoviePhotoSerializer(ModelSerializer):


    class Meta:
        model = MoviePhoto
        fields = [
            'file',
            'downloaded_url',
            'photo_code',
        ]


class MovieSerializer(ModelSerializer):
    code = serializers.CharField(source='movie_code.code', read_only=True)
    photos = MoviePhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = [
           'code',
           'title',
           'story_line',
           'rating_value',
           'rating_count',
           'photos',
        ]
