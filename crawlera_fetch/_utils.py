from logging import Logger
from typing import Optional, Union

from scrapy import Request, Spider
from scrapy.utils.python import global_object_name


# disable black formatting to avoid syntax error on py35
# fmt: off
def _get_retry_request(
    request: Request,
    *,
    spider: Spider,
    reason: Union[str, Exception] = "unspecified",
    max_retry_times: Optional[int] = None,
    priority_adjust: Optional[int] = None,
    logger: Logger,
    stats_base_key: str  # black wants to put a comma at the end, but py35 doesn't like it
) -> Optional[Request]:
    # fmt: on
    """
    Fallback implementation, taken verbatim from https://github.com/scrapy/scrapy/pull/4902
    """
    settings = spider.crawler.settings
    stats = spider.crawler.stats
    retry_times = request.meta.get("retry_times", 0) + 1
    if max_retry_times is None:
        max_retry_times = request.meta.get("max_retry_times")
        if max_retry_times is None:
            max_retry_times = settings.getint("RETRY_TIMES")
    if retry_times <= max_retry_times:
        logger.debug(
            "Retrying %(request)s (failed %(retry_times)d times): %(reason)s",
            {"request": request, "retry_times": retry_times, "reason": reason},
            extra={"spider": spider},
        )
        new_request = request.copy()
        new_request.meta["retry_times"] = retry_times
        new_request.dont_filter = True
        if priority_adjust is None:
            priority_adjust = settings.getint("RETRY_PRIORITY_ADJUST")
        new_request.priority = request.priority + priority_adjust

        if callable(reason):
            reason = reason()
        if isinstance(reason, Exception):
            reason = global_object_name(reason.__class__)

        stats.inc_value("{}/count".format(stats_base_key))
        stats.inc_value("{}/reason_count/{}".format(stats_base_key, reason))
        return new_request
    else:
        stats.inc_value("{}/max_reached".format(stats_base_key))
        logger.error(
            "Gave up retrying %(request)s (failed %(retry_times)d times): " "%(reason)s",
            {"request": request, "retry_times": retry_times, "reason": reason},
            extra={"spider": spider},
        )
        return None
