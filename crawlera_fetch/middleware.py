import json
import logging
from typing import Optional, Type, TypeVar

from scrapy import version_info as scrapy_version
from scrapy.crawler import Crawler
from scrapy.exceptions import NotConfigured
from scrapy.http.request import Request
from scrapy.http.response import Response
from scrapy.responsetypes import responsetypes
from scrapy.spiders import Spider
from w3lib.http import basic_auth_header


logger = logging.getLogger("crawlera-fetch-middleware")


MiddlewareTypeVar = TypeVar("MiddlewareTypeVar", bound="CrawleraFetchMiddleware")


class CrawleraFetchMiddleware:

    url = "https://api.crawlera.com/fetch/v2"
    apikey = ""

    def __init__(self, crawler: Crawler) -> None:
        if not crawler.settings.getbool("CRAWLERA_ENABLED"):
            raise NotConfigured()
        elif not crawler.settings.get("CRAWLERA_APIKEY"):
            raise NotConfigured("Crawlera cannot be used without an apikey")
        else:
            self.apikey = crawler.settings["CRAWLERA_APIKEY"]
            self.auth_header = basic_auth_header(self.apikey, "")

        if crawler.settings.get("CRAWLERA_URL"):
            self.url = crawler.settings["CRAWLERA_URL"]

        logger.debug("Using Crawlera at %s with apikey %s***" % (self.url, self.apikey[:5]))

    @classmethod
    def from_crawler(cls: Type[MiddlewareTypeVar], crawler: Crawler) -> MiddlewareTypeVar:
        return cls(crawler)

    def process_request(self, request: Request, spider: Spider) -> Optional[Request]:
        if request.meta.get("crawlera_processed"):
            return None
        request.meta["crawlera_processed"] = True

        crawlera_meta = request.meta.get("crawlera") or {}
        original_body_text = request.body.decode(request.encoding)
        body = {"url": request.url, "method": request.method, "body": original_body_text}
        body.update(crawlera_meta)

        headers = request.headers
        headers.update(
            {
                "Authorization": self.auth_header,
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )

        if scrapy_version < (2, 0, 0):
            request.flags.append("Original URL: {}".format(request.url))

        return request.replace(
            url=self.url, method="POST", headers=headers, body=json.dumps(body),
        )

    def process_response(self, request: Request, response: Response, spider: Spider) -> Response:
        request.meta.pop("crawlera_processed", None)
        json_response = json.loads(response.text)
        request.meta["crawlera_response"] = {
            "status": response.status,
            "headers": response.headers,
            "body": json_response,
        }
        respcls = responsetypes.from_args(
            headers=json_response["headers"], url=json_response["url"], body=json_response["body"],
        )
        return response.replace(
            cls=respcls,
            headers=json_response["headers"],
            url=json_response["url"],
            body=json_response["body"],
            status=json_response["original_status"],
        )
