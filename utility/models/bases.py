from django.db import models

from .managers import ActiveManager



class CreateHistoryModelMixin(models.Model):
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ایجاد'
    )

    class Meta:
        abstract = True


class UpdateHistoryModelMixin(models.Model):
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='تاریخ بروزرسانی'
    )

    class Meta:
        abstract = True


class SoftDeleteModelMixin(models.Model):
    all_objects = models.Manager()
    objects = ActiveManager()

    is_deleted = models.BooleanField(
        default=False,
        verbose_name='آیا حذف شده است؟',
        db_index=True,
    )

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save(update_fields=['is_deleted'])

    def hard_delete(self, using=None, keep_parents=False):
        super().delete(using, keep_parents)

    class Meta:
        abstract = True


class BaseModel(models.Model):
    objects = models.Manager()

    @property
    def meta(self):
        return self._meta

    @property
    def instance_from_db(self):
        return self.__class__.objects.filter(pk=self.pk).first()

    @classmethod
    def get_field(cls, field):
        return cls._meta.get_field(field)

    class Meta:
        abstract = True

