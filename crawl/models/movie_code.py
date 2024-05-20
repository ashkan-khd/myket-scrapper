import typing
from django.db import models
from utility.models import (
    CreateHistoryModelMixin,
    SoftDeleteModelMixin,
    BaseModel,
)
from utility.models import Choices

if typing.TYPE_CHECKING:
    from crawl.crawling import MovieCodeCrawler
    


class MovieCode(CreateHistoryModelMixin, SoftDeleteModelMixin, BaseModel):
    class CrawlStatus(Choices):
        NOT_CRAWLED = Choices.Choice("not crawled", "کرال نشده")
        CRAWL_FAILURE = Choices.Choice("crawl failure", "کرال با شکست")
        WRONG_CODE = Choices.Choice("wrong code", "کد اشتباه")
        CRAWLED_SUCCESSFULLY = Choices.Choice("craw successfully", "کرال با موفقیت")

    code = models.CharField(
        max_length=32,
        unique=True,
        db_index=True,
    )

    crawl_status = models.CharField(
        max_length=256,
        choices=CrawlStatus.get_choices(),
        default=CrawlStatus.NOT_CRAWLED,
        db_index=True,
    )

    last_crawl = models.DateTimeField(
        verbose_name='زمان آخرین کرال',
        null=True, blank=True,
    )

    def get_crawler(self) -> 'MovieCodeCrawler':
        from crawl.crawling import MovieCodeCrawler
        return MovieCodeCrawler(self)

    class Meta:
        verbose_name = ""
        verbose_name_plural = ""
