from rest_framework.mixins import RetrieveModelMixin
from rest_framework.settings import api_settings
from rest_framework.viewsets import GenericViewSet

from crawl.models import MovieCode, Movie
from crawl.serializers import MovieSerializer, MovieCodeSerializer


class GetMovieCodeView(RetrieveModelMixin, GenericViewSet):
    queryset = MovieCode.objects.all()
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + []
    lookup_field = "code"
    lookup_url_kwarg = "code"
    serializer_class = MovieCodeSerializer


class GetMovieView(RetrieveModelMixin, GenericViewSet):
    queryset = Movie.objects.all()
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + []
    lookup_field = "title"
    lookup_url_kwarg = "title"
    serializer_class = MovieSerializer
