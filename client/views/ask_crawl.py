from rest_framework.mixins import CreateModelMixin
from rest_framework.settings import api_settings
from rest_framework.viewsets import GenericViewSet

from crawl.models import MovieCode, Movie
from crawl.serializers import MovieCodeDeserializer



class AskCrawlView(CreateModelMixin, GenericViewSet):
    queryset = MovieCode.objects.all()
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + []
    serializer_class = MovieCodeDeserializer

    def perform_create(self, serializer):
        movie_code: MovieCode = serializer.save()
        crawler = movie_code.get_crawler()
        crawler.start_crawling()
