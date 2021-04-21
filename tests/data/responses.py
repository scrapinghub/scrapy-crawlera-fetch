import base64
import json

from scrapy.http.request import Request
from scrapy.http.response.html import HtmlResponse
from scrapy.http.response.text import TextResponse
from scrapy.utils.reqser import request_to_dict

from tests.data import SETTINGS
from tests.utils import foo_spider, mocked_time


def get_test_responses(include_unprocessed=True):
    test_responses = []

    test_responses.append(
        {
            "original": HtmlResponse(
                url=SETTINGS["CRAWLERA_FETCH_URL"],
                status=200,
                headers={
                    "Content-Type": "application/json",
                    "Content-Encoding": "gzip",
                    "Transfer-Encoding": "chunked",
                    "Date": "Fri, 24 Apr 2020 18:06:42 GMT",
                    "Proxy-Connection": "close",
                    "Connection": "close",
                },
                request=Request(
                    url=SETTINGS["CRAWLERA_FETCH_URL"],
                    meta={
                        "crawlera_fetch": {
                            "timing": {"start_ts": mocked_time()},
                            "original_request": request_to_dict(
                                Request("https://fake.host.com"),
                                spider=foo_spider,
                            ),
                        }
                    },
                ),
                body=b"""{"url":"https://fake.host.com","original_status":123,"headers":{"fake-header":"true"},"body":"foobar"}""",  # noqa: E501
            ),
            "expected": TextResponse(
                url="https://fake.host.com",
                status=123,
                headers={"Fake-Header": "true"},
                body=b"""foobar""",  # noqa: E501
            ),
        }
    )

    test_responses.append(
        {
            "original": HtmlResponse(
                url=SETTINGS["CRAWLERA_FETCH_URL"],
                status=200,
                headers={
                    "Content-Type": "application/json",
                    "Content-Encoding": "gzip",
                    "Transfer-Encoding": "chunked",
                    "Date": "Fri, 24 Apr 2020 18:06:42 GMT",
                    "Proxy-Connection": "close",
                    "Connection": "close",
                },
                request=Request(
                    url=SETTINGS["CRAWLERA_FETCH_URL"],
                    meta={
                        "crawlera_fetch": {
                            "timing": {"start_ts": mocked_time()},
                            "original_request": request_to_dict(
                                Request("https://httpbin.org/get"),
                                spider=foo_spider,
                            ),
                        }
                    },
                ),
                body=b"""{"url":"https://httpbin.org/get","original_status":200,"headers":{"X-Crawlera-Slave":"196.16.27.20:8800","X-Crawlera-Version":"1.43.0-","status":"200","date":"Fri, 24 Apr 2020 18:06:42 GMT","content-type":"application/json","content-length":"756","server":"gunicorn/19.9.0","access-control-allow-origin":"*","access-control-allow-credentials":"true"},"crawlera_status":"success","body_encoding":"plain","body":"<html><head></head><body><pre style=\\"word-wrap: break-word; white-space: pre-wrap;\\">{\\n  \\"args\\": {}, \\n  \\"headers\\": {\\n    \\"Accept\\": \\"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\\", \\n    \\"Accept-Encoding\\": \\"gzip, deflate, br\\", \\n    \\"Accept-Language\\": \\"en-US,en;q=0.9\\", \\n    \\"Cache-Control\\": \\"no-cache\\", \\n    \\"Host\\": \\"httpbin.org\\", \\n    \\"Pragma\\": \\"no-cache\\", \\n    \\"Sec-Fetch-Mode\\": \\"navigate\\", \\n    \\"Sec-Fetch-Site\\": \\"none\\", \\n    \\"Sec-Fetch-User\\": \\"?1\\", \\n    \\"Upgrade-Insecure-Requests\\": \\"1\\", \\n    \\"User-Agent\\": \\"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.44 Safari/537.36\\", \\n    \\"X-Amzn-Trace-Id\\": \\"Root=1-5ea32ab2-93f521ee8238c744c88e3fec\\"\\n  }, \\n  \\"origin\\": \\"173.0.152.100\\", \\n  \\"url\\": \\"https://httpbin.org/get\\"\\n}\\n</pre></body></html>"}""",  # noqa: E501
            ),
            "expected": HtmlResponse(
                url="https://httpbin.org/get",
                status=200,
                headers={
                    "X-Crawlera-Slave": "196.16.27.20:8800",
                    "X-Crawlera-Version": "1.43.0-",
                    "status": "200",
                    "date": "Fri, 24 Apr 2020 18:06:42 GMT",
                    "content-type": "application/json",
                    "content-length": "756",
                    "server": "gunicorn/19.9.0",
                    "access-control-allow-origin": "*",
                    "access-control-allow-credentials": "true",
                },
                body=b"""<html><head></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">{\n  "args": {}, \n  "headers": {\n    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", \n    "Accept-Encoding": "gzip, deflate, br", \n    "Accept-Language": "en-US,en;q=0.9", \n    "Cache-Control": "no-cache", \n    "Host": "httpbin.org", \n    "Pragma": "no-cache", \n    "Sec-Fetch-Mode": "navigate", \n    "Sec-Fetch-Site": "none", \n    "Sec-Fetch-User": "?1", \n    "Upgrade-Insecure-Requests": "1", \n    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.44 Safari/537.36", \n    "X-Amzn-Trace-Id": "Root=1-5ea32ab2-93f521ee8238c744c88e3fec"\n  }, \n  "origin": "173.0.152.100", \n  "url": "https://httpbin.org/get"\n}\n</pre></body></html>""",  # noqa: E501
            ),
        }
    )

    test_responses.append(
        {
            "original": HtmlResponse(
                url=SETTINGS["CRAWLERA_FETCH_URL"],
                status=200,
                headers={
                    "Content-Type": "application/json",
                    "Content-Encoding": "gzip",
                    "Transfer-Encoding": "chunked",
                    "Date": "Fri, 24 Apr 2020 18:22:10 GMT",
                    "Proxy-Connection": "close",
                    "Connection": "close",
                },
                request=Request(
                    url=SETTINGS["CRAWLERA_FETCH_URL"],
                    meta={
                        "crawlera_fetch": {
                            "timing": {"start_ts": mocked_time()},
                            "original_request": request_to_dict(
                                Request("https://example.org"),
                                spider=foo_spider,
                            ),
                        }
                    },
                ),
                body=b"""{"url":"https://example.org","original_status":200,"headers":{"X-Crawlera-Slave":"192.241.80.236:3128","X-Crawlera-Version":"1.43.0-","status":"200","content-encoding":"gzip","accept-ranges":"bytes","age":"108944","cache-control":"max-age=604800","content-type":"text/html; charset=UTF-8","date":"Fri, 24 Apr 2020 18:22:10 GMT","etag":"\\"3147526947\\"","expires":"Fri, 01 May 2020 18:22:10 GMT","last-modified":"Thu, 17 Oct 2019 07:18:26 GMT","server":"ECS (dab/4B85)","vary":"Accept-Encoding","content-length":"648"},"crawlera_status":"success","body_encoding":"plain","body":"<!DOCTYPE html><html><head>\\n    <title>Example Domain</title>\\n\\n    <meta charset=\\"utf-8\\">\\n    <meta http-equiv=\\"Content-type\\" content=\\"text/html; charset=utf-8\\">\\n    <meta name=\\"viewport\\" content=\\"width=device-width, initial-scale=1\\">\\n    <style type=\\"text/css\\">\\n    body {\\n        background-color: #f0f0f2;\\n        margin: 0;\\n        padding: 0;\\n        font-family: -apple-system, system-ui, BlinkMacSystemFont, \\"Segoe UI\\", \\"Open Sans\\", \\"Helvetica Neue\\", Helvetica, Arial, sans-serif;\\n        \\n    }\\n    div {\\n        width: 600px;\\n        margin: 5em auto;\\n        padding: 2em;\\n        background-color: #fdfdff;\\n        border-radius: 0.5em;\\n        box-shadow: 2px 3px 7px 2px rgba(0,0,0,0.02);\\n    }\\n    a:link, a:visited {\\n        color: #38488f;\\n        text-decoration: none;\\n    }\\n    @media (max-width: 700px) {\\n        div {\\n            margin: 0 auto;\\n            width: auto;\\n        }\\n    }\\n    </style>    \\n</head>\\n\\n<body>\\n<div>\\n    <h1>Example Domain</h1>\\n    <p>This domain is for use in illustrative examples in documents. You may use this\\n    domain in literature without prior coordination or asking for permission.</p>\\n    <p><a href=\\"https://www.iana.org/domains/example\\">More information...</a></p>\\n</div>\\n\\n\\n</body></html>"}""",  # noqa: E501
            ),
            "expected": HtmlResponse(
                url="https://example.org",
                status=200,
                headers={
                    "X-Crawlera-Slave": "192.241.80.236:3128",
                    "X-Crawlera-Version": "1.43.0-",
                    "status": "200",
                    "content-encoding": "gzip",
                    "accept-ranges": "bytes",
                    "age": "108944",
                    "cache-control": "max-age=604800",
                    "content-type": "text/html; charset=UTF-8",
                    "date": "Fri, 24 Apr 2020 18:22:10 GMT",
                    "etag": '"3147526947"',
                    "expires": "Fri, 01 May 2020 18:22:10 GMT",
                    "last-modified": "Thu, 17 Oct 2019 07:18:26 GMT",
                    "server": "ECS (dab/4B85)",
                    "vary": "Accept-Encoding",
                    "content-length": "648",
                },
                body=b"""<!DOCTYPE html><html><head>\n    <title>Example Domain</title>\n\n    <meta charset="utf-8">\n    <meta http-equiv="Content-type" content="text/html; charset=utf-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1">\n    <style type="text/css">\n    body {\n        background-color: #f0f0f2;\n        margin: 0;\n        padding: 0;\n        font-family: -apple-system, system-ui, BlinkMacSystemFont, "Segoe UI", "Open Sans", "Helvetica Neue", Helvetica, Arial, sans-serif;\n        \n    }\n    div {\n        width: 600px;\n        margin: 5em auto;\n        padding: 2em;\n        background-color: #fdfdff;\n        border-radius: 0.5em;\n        box-shadow: 2px 3px 7px 2px rgba(0,0,0,0.02);\n    }\n    a:link, a:visited {\n        color: #38488f;\n        text-decoration: none;\n    }\n    @media (max-width: 700px) {\n        div {\n            margin: 0 auto;\n            width: auto;\n        }\n    }\n    </style>    \n</head>\n\n<body>\n<div>\n    <h1>Example Domain</h1>\n    <p>This domain is for use in illustrative examples in documents. You may use this\n    domain in literature without prior coordination or asking for permission.</p>\n    <p><a href="https://www.iana.org/domains/example">More information...</a></p>\n</div>\n\n\n</body></html>""",  # noqa: E501
            ),
        }
    )

    response_body_test = b"<html>Hello middleware test!</html>"
    test_responses.append(
        {
            "original": HtmlResponse(
                url=SETTINGS["CRAWLERA_FETCH_URL"],
                status=200,
                headers={
                    "Content-Type": "application/json",
                    "Content-Encoding": "gzip",
                    "Date": "Fri, 24 Apr 2020 18:22:10 GMT",
                },
                request=Request(
                    url=SETTINGS["CRAWLERA_FETCH_URL"],
                    meta={
                        "crawlera_fetch": {
                            "timing": {"start_ts": mocked_time()},
                            "original_request": request_to_dict(
                                Request("http://httpbin.org/ip"),
                                spider=foo_spider,
                            ),
                        }
                    },
                ),
                body=json.dumps(
                    {
                        "id": "8498642e-1de3-40dd-b32f-f6eb6131e45e",
                        "body": base64.b64encode(response_body_test).decode(),
                        "original_status": 200,
                        "url": "http://httpbin.org/ip",
                        "original_url": "http://httpbin.org/ip",
                        "headers": {
                            "Content-Encoding": "gzip",
                            "Content-Type": "text/html",
                            "Date": "Fri, 24 Apr 2020 18:06:42 GMT",
                        },
                    }
                ).encode(),
            ),
            "expected": HtmlResponse(
                url="http://httpbin.org/ip",
                status=200,
                headers={
                    "content-encoding": "gzip",
                    "content-type": "text/html",
                    "date": "Fri, 24 Apr 2020 18:06:42 GMT",
                },
                body=response_body_test,
            ),
        }
    )

    if include_unprocessed:
        unprocessed = HtmlResponse(
            url="https://example.org",
            status=200,
            headers={
                "Content-Type": "text/html",
                "Content-Encoding": "gzip",
                "Transfer-Encoding": "chunked",
                "Date": "Fri, 24 Apr 2020 18:06:42 GMT",
            },
            request=Request("https://example.org"),
            body=b"""<html></html>""",
        )
        test_responses.append({"original": unprocessed, "expected": unprocessed})

    return test_responses


def get_test_responses_error():
    return [
        TextResponse(
            url="https://crawlera.com/fake/api/endpoint",
            request=Request(
                url="https://crawlera.com/fake/api/endpoint",
                meta={
                    "crawlera_fetch": {
                        "timing": {"start_ts": mocked_time()},
                        "original_request": request_to_dict(
                            Request("https://example.org"),
                            spider=foo_spider,
                        ),
                    }
                },
            ),
            headers={
                "X-Crawlera-Error": "bad_proxy_auth",
                "Proxy-Authenticate": 'Basic realm="Crawlera"',
                "Content-Length": "0",
                "Date": "Mon, 04 May 2020 13:06:15 GMT",
                "Proxy-Connection": "close",
                "Connection": "close",
            },
        ),
        TextResponse(
            url="https://crawlera.com/fake/api/endpoint",
            request=Request(
                url="https://crawlera.com/fake/api/endpoint",
                meta={
                    "crawlera_fetch": {
                        "timing": {"start_ts": mocked_time()},
                        "original_request": request_to_dict(
                            Request("https://example.org"),
                            spider=foo_spider,
                        ),
                    }
                },
            ),
            body=b'{"Bad": "JSON',
        ),
        TextResponse(
            url="https://crawlera.com/fake/api/endpoint",
            request=Request(
                url="https://crawlera.com/fake/api/endpoint",
                meta={
                    "crawlera_fetch": {
                        "timing": {"start_ts": mocked_time()},
                        "original_request": request_to_dict(
                            Request("https://example.org"),
                            spider=foo_spider,
                        ),
                    }
                },
            ),
            body=json.dumps(
                {
                    "url": "https://example.org",
                    "original_status": 503,
                    "headers": {},
                    "crawlera_status": "fail",
                    "crawlera_error": "serverbusy",
                    "body_encoding": "plain",
                    "body": "Server busy: too many outstanding requests",
                }
            ),
            encoding="utf8",
        ),
    ]
