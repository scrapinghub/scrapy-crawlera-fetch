import json

from scrapy import Request, FormRequest
from scrapy.utils.reqser import request_to_dict
from w3lib.http import basic_auth_header

from tests.data import SETTINGS
from tests.utils import foo_spider, mocked_time


def get_test_requests():
    test_requests = []

    original1 = Request(
        url="https://httpbin.org/anything",
        method="GET",
        meta={
            "zyte_proxy_fetch": {
                "args": {
                    "render": "no",
                    "region": "us",
                    "iptype": "datacenter",
                    "device": "mobile",
                }
            }
        },
    )
    expected1 = Request(
        url=SETTINGS["ZYTE_PROXY_FETCH_URL"],
        callback=foo_spider.foo_callback,
        method="POST",
        headers={
            "Authorization": basic_auth_header(
                SETTINGS["ZYTE_PROXY_FETCH_APIKEY"], SETTINGS["ZYTE_PROXY_FETCH_APIPASS"]
            ),
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-Crawlera-JobId": "1/2/3",
        },
        meta={
            "zyte_proxy_fetch": {
                "args": {
                    "render": "no",
                    "region": "us",
                    "iptype": "datacenter",
                    "device": "mobile",
                },
                "original_request": request_to_dict(original1, spider=foo_spider),
                "timing": {"start_ts": mocked_time()},
            },
            "download_slot": "httpbin.org",
        },
        body=json.dumps(
            {
                "url": "https://httpbin.org/anything",
                "body": "",
                "render": "no",
                "region": "us",
                "iptype": "datacenter",
                "device": "mobile",
                "job_id": "1/2/3",
            }
        ),
    )
    test_requests.append(
        {
            "original": original1,
            "expected": expected1,
        }
    )

    original2 = FormRequest(
        url="https://httpbin.org/post",
        callback=foo_spider.foo_callback,
        meta={"zyte_proxy_fetch": {"args": {"device": "desktop"}}},
        formdata={"foo": "bar"},
    )
    expected2 = FormRequest(
        url=SETTINGS["ZYTE_PROXY_FETCH_URL"],
        method="POST",
        headers={
            "Authorization": basic_auth_header(
                SETTINGS["ZYTE_PROXY_FETCH_APIKEY"], SETTINGS["ZYTE_PROXY_FETCH_APIPASS"]
            ),
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-Crawlera-JobId": "1/2/3",
        },
        meta={
            "zyte_proxy_fetch": {
                "args": {"device": "desktop"},
                "original_request": request_to_dict(original2, spider=foo_spider),
                "timing": {"start_ts": mocked_time()},
            },
            "download_slot": "httpbin.org",
        },
        body=json.dumps(
            {
                "url": "https://httpbin.org/post",
                "method": "POST",
                "body": "foo=bar",
                "device": "desktop",
                "job_id": "1/2/3",
            }
        ),
    )
    test_requests.append(
        {
            "original": original2,
            "expected": expected2,
        }
    )

    test_requests.append(
        {
            "original": Request(
                url="https://example.org",
                method="HEAD",
                meta={"zyte_proxy_fetch": {"skip": True}},
            ),
            "expected": None,
        }
    )

    return test_requests
