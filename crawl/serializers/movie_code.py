from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer

from crawl.models import MovieCode
from .movie import MovieSerializer


class MovieCodeDeserializer(Serializer):
    code = serializers.CharField(max_length=32)

    def create(self, validated_data):
        return MovieCode.objects.get_or_create(
            defaults=dict(code=validated_data["code"])
        )

    class Meta:
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
