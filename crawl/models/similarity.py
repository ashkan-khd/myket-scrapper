


from django.db import models
from utility.models import BaseModel


class MovieSimilarity(BaseModel):

    the_case = models.ForeignKey(
        to="crwal.MovieCode",
        related_name="more_like_this",
        on_delete=models.CASCADE,
        verbose_name="فیلم مربوطه",
    )

    is_similar_to = models.ForeignKey(
        to="crwal.MovieCode",
        related_name="similar_to",
        on_delete=models.CASCADE,
        verbose_name="فیلم مربوطه",
    )

    class Meta:
        verbose_name = ''
        verbose_name_plural = ''
