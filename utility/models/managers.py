from django.db import models
from django.db.models import QuerySet


def filter_active_objects(queryset) -> QuerySet:
    return queryset.filter(is_deleted=False)


class ActiveManager(models.Manager):
    def get_queryset(self):
        return filter_active_objects(super().get_queryset())
