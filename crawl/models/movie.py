from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from utility.models import (
    CreateHistoryModelMixin,
    UpdateHistoryModelMixin,
    SoftDeleteModelMixin,
    BaseModel,
)


class Movie(
    CreateHistoryModelMixin, UpdateHistoryModelMixin, SoftDeleteModelMixin, BaseModel
):

    movie_code = models.OneToOneField(
        to="crawl.MovieCode",
        on_delete=models.PROTECT,
        related_name="crawled_movie",
        verbose_name="کد IMDB",
    )

    title = models.CharField(max_length=256, verbose_name="عنوان فیلم")

    story_line = models.TextField(verbose_name="توضیحات")

    rating_value = models.FloatField(
        verbose_name="رنکینگ",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10),
        ],
    )

    rating_count = models.PositiveBigIntegerField(
        verbose_name="تعداد نمره‌دهندگان",
    )

    class Meta:
        verbose_name = ""
        verbose_name_plural = ""
