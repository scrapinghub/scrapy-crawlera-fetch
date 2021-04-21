import json

import pytest
from scrapy import Request
from scrapy.http.response.text import TextResponse
from testfixtures import LogCapture

from crawlera_fetch.middleware import CrawleraFetchException, OnError

from tests.data.responses import get_test_responses, get_test_responses_error
from tests.utils import foo_spider, get_test_middleware


def test_process_response_disabled():
    middleware = get_test_middleware(settings={"CRAWLERA_FETCH_ENABLED": False})
    for case in get_test_responses():
        response = case["original"]
        assert middleware.process_response(response.request, response, foo_spider) is response


def test_process_response():
    middleware = get_test_middleware()

    for case in get_test_responses():
        original = case["original"]
        expected = case["expected"]

        processed = middleware.process_response(original.request, original, foo_spider)

        assert type(processed) is type(expected)
        assert processed.url == expected.url
        assert processed.status == expected.status
        assert processed.headers == expected.headers
        assert processed.body == expected.body

        crawlera_meta = processed.meta.get("crawlera_fetch") or {}
        if crawlera_meta.get("upstream_response"):
            assert crawlera_meta["upstream_response"]["body"] == json.loads(original.text)
            assert crawlera_meta["upstream_response"]["headers"] == original.headers
            assert crawlera_meta["upstream_response"]["status"] == original.status


def test_process_response_skip():
    response = TextResponse(
        url="https://example.org",
        status=200,
        headers={
            "Content-Encoding": "gzip",
            "Transfer-Encoding": "chunked",
            "Date": "Fri, 24 Apr 2020 18:06:42 GMT",
        },
        request=Request(
            url="https://example.org",
            meta={"crawlera_fetch": {"skip": True}},
        ),
        body=b"""<html></html>""",
    )

    middleware = get_test_middleware()
    processed = middleware.process_response(response.request, response, foo_spider)

    assert response is processed


def test_process_response_error():
    middleware = get_test_middleware(settings={"CRAWLERA_FETCH_ON_ERROR": OnError.Raise})
    for response in get_test_responses_error():
        with pytest.raises(CrawleraFetchException):
            middleware.process_response(response.request, response, foo_spider)

    assert middleware.stats.get_value("crawlera_fetch/response_error") == 3
    assert middleware.stats.get_value("crawlera_fetch/response_error/bad_proxy_auth") == 1
    assert middleware.stats.get_value("crawlera_fetch/response_error/JSONDecodeError") == 1
    assert middleware.stats.get_value("crawlera_fetch/response_error/serverbusy") == 1


def test_process_response_warn():
    with LogCapture() as logs:
        middleware = get_test_middleware(settings={"CRAWLERA_FETCH_ON_ERROR": OnError.Warn})
        for response in get_test_responses_error():
            processed = middleware.process_response(response.request, response, foo_spider)
            assert response is processed

    logs.check_present(
        (
            "crawlera-fetch-middleware",
            "WARNING",
            "Error downloading <GET https://example.org> (status: 200, X-Crawlera-Error header: bad_proxy_auth)",  # noqa: E501
        ),
        (
            "crawlera-fetch-middleware",
            "WARNING",
            "Error decoding <GET https://example.org> (status: 200, message: Unterminated string starting at, lineno: 1, colno: 9)",  # noqa: E501
        ),
        (
            "crawlera-fetch-middleware",
            "WARNING",
            "Error downloading <GET https://example.org> (Original status: 503, Fetch API error message: Server busy: too many outstanding requests, Request ID: unknown)",  # noqa: E501
        ),
    )

    assert middleware.stats.get_value("crawlera_fetch/response_error") == 3
    assert middleware.stats.get_value("crawlera_fetch/response_error/bad_proxy_auth") == 1
    assert middleware.stats.get_value("crawlera_fetch/response_error/JSONDecodeError") == 1
    assert middleware.stats.get_value("crawlera_fetch/response_error/serverbusy") == 1


def test_process_response_error_deprecated():
    middleware = get_test_middleware(settings={"CRAWLERA_FETCH_RAISE_ON_ERROR": True})
    for response in get_test_responses_error():
        with pytest.raises(CrawleraFetchException):
            middleware.process_response(response.request, response, foo_spider)

    assert middleware.stats.get_value("crawlera_fetch/response_error") == 3
    assert middleware.stats.get_value("crawlera_fetch/response_error/bad_proxy_auth") == 1
    assert middleware.stats.get_value("crawlera_fetch/response_error/JSONDecodeError") == 1
    assert middleware.stats.get_value("crawlera_fetch/response_error/serverbusy") == 1


def test_process_response_warn_deprecated():
    with LogCapture() as logs:
        middleware = get_test_middleware(settings={"CRAWLERA_FETCH_RAISE_ON_ERROR": False})
        for response in get_test_responses_error():
            processed = middleware.process_response(response.request, response, foo_spider)
            assert response is processed

    logs.check_present(
        (
            "crawlera-fetch-middleware",
            "WARNING",
            "Error downloading <GET https://example.org> (status: 200, X-Crawlera-Error header: bad_proxy_auth)",  # noqa: E501
        ),
        (
            "crawlera-fetch-middleware",
            "WARNING",
            "Error decoding <GET https://example.org> (status: 200, message: Unterminated string starting at, lineno: 1, colno: 9)",  # noqa: E501
        ),
        (
            "crawlera-fetch-middleware",
            "WARNING",
            "Error downloading <GET https://example.org> (Original status: 503, Fetch API error message: Server busy: too many outstanding requests, Request ID: unknown)",  # noqa: E501
        ),
    )

    assert middleware.stats.get_value("crawlera_fetch/response_error") == 3
    assert middleware.stats.get_value("crawlera_fetch/response_error/bad_proxy_auth") == 1
    assert middleware.stats.get_value("crawlera_fetch/response_error/JSONDecodeError") == 1
    assert middleware.stats.get_value("crawlera_fetch/response_error/serverbusy") == 1
