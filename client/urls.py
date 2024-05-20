from django.urls import path

from client.views import GetMovieView, GetMovieCodeView, AskCrawlView

urlpatterns = [
    path(
        "movie-code/<str:code>/",
        GetMovieCodeView.as_view(
            {
                "get": "retrieve",
            }
        ),
    ),
    path(
        "movie/<str:title>/",
        GetMovieView.as_view(
            {
                "get": "retrieve",
            }
        ),
    ),
    path(
        "crawl/",
        AskCrawlView.as_view(
            {
                "post": "create",
            }
        ),
    ),
]
