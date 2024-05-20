from abc import ABC, abstractmethod
import json
from bs4 import BeautifulSoup


class IMDBCrawlerInterfaceWithSoup(ABC):
    soup: BeautifulSoup

    @abstractmethod
    def crawl_element(self) -> dict:
        pass


class IMDBBaseCrawler(IMDBCrawlerInterfaceWithSoup, ABC):
    def __init__(self, soup: BeautifulSoup) -> None:
        super().__init__()
        self.soup = soup


class IMDBTitleCrawler(IMDBBaseCrawler):

    def crawl_element(self) -> dict:
        movie_name = self.soup.find("h1").text.strip()
        return dict(movie_name=movie_name)


class IMDBRatingDescriptionCrawler(IMDBBaseCrawler):
    def crawl_element(self) -> dict:
        script_tag = self.soup.find("script", type="application/ld+json")
        json_data = json.loads(script_tag.string)

        movie_description = json_data.get("description", "N/A")
        rating_value = json_data.get("aggregateRating", {}).get("ratingValue", "N/A")
        rating_count = json_data.get("aggregateRating", {}).get("ratingCount", "N/A")
        return dict(
            movie_description=movie_description,
            rating_value=rating_value,
            rating_count=rating_count,
        )


class IMDBPhotoCrawler(IMDBBaseCrawler):
    def crawl_element(self) -> dict:
        next_data_script = self.soup.find("script", {"id": "__NEXT_DATA__"})
        next_data_json = json.loads(next_data_script.string)

        photos = []
        if next_data_json is not None:
            edges = next_data_json["props"]["pageProps"]["mainColumnData"][
                "titleMainImages"
            ]["edges"]
            for i in range(min(3, len(edges))):
                photos.append({
                    'url': edges[i]["node"]["url"],
                    'code': edges[i]["node"]["id"],
                })

        return dict(photos=photos)


class IMDBSimilarsCrawler(IMDBBaseCrawler):
    def crawl_element(self) -> dict:
        more_like_this_section = self.soup.find_all("div", {"class": "ipc-poster-card"})
        more_like_this = []
        for card in more_like_this_section:
            more_like_this.append(card.a["href"].split("/")[2])
        return dict(similar_codes=more_like_this)
