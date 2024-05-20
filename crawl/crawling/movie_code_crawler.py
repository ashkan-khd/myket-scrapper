from dataclasses import dataclass
import typing

from bs4 import BeautifulSoup
import requests

from django.utils import timezone
from django.db import transaction
from crawl.models import MovieCode

from .imdb_request import IMDBCodeRequest
from .crawled_data import CrawledMovie, CrawledPhoto

if typing.TYPE_CHECKING:
    from .imdb_request import IMDBRequestInterface
    from .imdb_crawler import IMDBCrawlerInterfaceWithSoup


class MovieCodeCrawler:
    class CrawlException(Exception):
        pass

    def __init__(self, movie_code: MovieCode) -> None:
        self.movie_code = movie_code

    def _get_imdb_request(self) -> "IMDBRequestInterface":
        return IMDBCodeRequest(self.movie_code.code)

    def _request(
        self,
    ) -> typing.Tuple[typing.Optional[requests.Response], typing.Optional[Exception]]:
        imdb_request = self._get_imdb_request()
        try:
            response = imdb_request.request()
            return response, None
        except requests.exceptions.HTTPError as e:
            return None, e

    def _finalize_movie_code(self, crawl_status: MovieCode.CrawlStatus):
        self.movie_code.crawl_status = crawl_status
        self.movie_code.last_crawl = timezone.now()
        self.movie_code.save(update_fields=["crawl_status", "last_crawl"])

    def _get_crawlers(
        self, response: requests.Response
    ) -> typing.List["IMDBCrawlerInterfaceWithSoup"]:
        from crawl.crawling.imdb_crawler import (
            IMDBTitleCrawler,
            IMDBRatingDescriptionCrawler,
            IMDBPhotoCrawler,
            IMDBSimilarsCrawler,
        )

        soup = BeautifulSoup(response.content, "lxml")
        crawler_classes = [
            IMDBTitleCrawler,
            IMDBRatingDescriptionCrawler,
            IMDBPhotoCrawler,
            IMDBSimilarsCrawler,
        ]
        return [crawler_class(soup) for crawler_class in crawler_classes]

    def _crawl(self, response: requests.Response) -> typing.Optional[CrawledMovie]:
        crawlers = self._get_crawlers(response)
        try:
            result_dict = {}
            for crawler in crawlers:
                result_dict.update(crawler.crawl_element())
            photos = result_dict.pop("photos")
            photos_data = []
            for photo in photos:
                photos_data.append(CrawledPhoto(**photo))

            return CrawledMovie(
                **result_dict,
                photos=photos_data,
            )
        except:
            return None

    def start_crawling(self):
        if (
            self.movie_code.crawl_status
            == self.movie_code.CrawlStatus.CRAWLED_SUCCESSFULLY
        ):
            return

        resp, err = self._request()
        if err is not None:
            if "404" in str(err):
                self._finalize_movie_code(self.movie_code.CrawlStatus.WRONG_CODE)
            else:
                self._finalize_movie_code(self.movie_code.CrawlStatus.CRAWL_FAILURE)
            return
        assert resp is not None

        crawled_data = self._crawl(resp)
        if crawled_data is None:
            self._finalize_movie_code(self.movie_code.CrawlStatus.CRAWL_FAILURE)
            return

        with transaction.atomic():
            crawled_data.hard_create(movie_code=self.movie_code)
            self._finalize_movie_code(self.movie_code.CrawlStatus.CRAWLED_SUCCESSFULLY)
