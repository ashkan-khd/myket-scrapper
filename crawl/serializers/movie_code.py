from rest_framework.serializers import ModelSerializer

from crawl.models import MovieCode
from .movie import MovieSerializer


class MovieCodeDeserializer(ModelSerializer):

    class Meta:
        model = MovieCode
        fields = [
            "code",
        ]


class MovieCodeSerializer(ModelSerializer):
    crawled_movie = MovieSerializer(read_only=True)

    class Meta:
        model = MovieCode
        fields = [
            "code",
            "crawl_status",
            "crawled_movie",
        ]
