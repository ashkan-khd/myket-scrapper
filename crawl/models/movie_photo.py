from django.db import models
from utility.models.bases import BaseModel
from utility.random import rand_slug


def movie_photo_upload_to(instance: "MoviePhoto", filename: str):
    return f"crawl/movie_photo/movie-{str(instance.movie.id)}-{filename}"


# TODO: Make sure to remove the photo file after deletion
class MoviePhoto(BaseModel):

    movie = models.ForeignKey(
        to="crawl.Movie",
        related_name="photos",
        on_delete=models.CASCADE,
        verbose_name="فیلم مربوطه",
    )

    file = models.FileField(
        upload_to=movie_photo_upload_to,
        verbose_name="فایل تصویر",
    )

    downloaded_url = models.URLField(
        verbose_name="آدرس دانلود شده",
        max_length=1048,
    )

    photo_code = models.CharField(verbose_name="کد عکس", max_length=32)

    @property
    def imdb_url(self) -> str:
        return f"https://www.imdb.com/title/tt0111161/mediaviewer/{self.photo_code}/"

    class Meta:
        verbose_name = ""
        verbose_name_plural = ""
