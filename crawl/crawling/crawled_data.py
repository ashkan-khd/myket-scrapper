import abc
import os
import typing

import requests
from django.core.files.base import ContentFile


from crawl.models import MovieCode, Movie, MoviePhoto, MovieSimilarity


class CrawledData(abc.ABC):

    @abc.abstractmethod
    def hard_create(self, **kwargs):
        pass


class CrawledPhoto(CrawledData):
    def __init__(self, code: str, url: str) -> None:
        self.code, self.url = code, url

    def hard_create(self, movie: Movie):
        response = requests.get(self.url)
        if response.status_code == 200:
            filename = os.path.basename(self.url)
            movie_photo = MoviePhoto.objects.create(
                movie=movie,
                file=ContentFile(response.content, name=filename),
                downloaded_url=self.url,
                photo_code=self.code,
            )
            return movie_photo
        else:
            # Handle error if the image could not be downloaded
            return None


class CrawledMovie(CrawledData):
    def __init__(
        self,
        movie_name: str,
        movie_description: str,
        rating_value: int,
        rating_count: int,
        photos: typing.List[CrawledPhoto],
        similar_codes: typing.List[str],
    ) -> None:
        super().__init__()
        self.movie_name = movie_name
        self.movie_description = movie_description
        self.rating_value = rating_value
        self.rating_count = rating_count
        self.photos = photos
        self.similar_codes = similar_codes

    def hard_create(self, movie_code: MovieCode):
        movie = Movie.objects.create(
            movie_code=movie_code,
            title=self.movie_name,
            story_line=self.movie_description,
            rating_value=self.rating_value,
            rating_count=self.rating_count,
        )
        for photo in self.photos:
            photo.hard_create(movie=movie)

        for similar_code in self.similar_codes:
            sim_movie_code, _ = MovieCode.objects.get_or_create(
                defaults=dict(code=similar_code)
            )
            MovieSimilarity.objects.create(
                the_case=movie_code,
                is_similar_to=sim_movie_code,
            )
