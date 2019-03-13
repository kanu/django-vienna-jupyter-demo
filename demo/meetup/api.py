import requests
import logging
from requests import Response
from time import sleep, time

from .models import MeetupGroup, MeetupEvent, MeetupMember


logger = logging.getLogger()
API_HOST = "https://api.meetup.com"


class RequestException(Exception):
    def __init__(self, response):
        super(RequestException, self).__init__(response.text)
        self.response = response


class Client(requests.Session):
    """
    Client for the meetup api with a simple strategy to stay within the rate
    limit.
    """
    def __init__(self, api_key: str):
        super().__init__()
        self.api_key = api_key
        self.rate_limit_until = 0
        self.rate_limit_exceeded = False

    def request(self, method: str, url: str, **kwargs) -> Response:
        url = f"{API_HOST}/{url}"
        params = kwargs.setdefault("params", {})
        if not "key" in params:
            params["key"] = self.api_key

        if self.rate_limit_exceeded:
            timeout = self.rate_limit_until  - time()
            if timeout > 0:
                logger.info("Meetup Api rate limit exceeded. waiting %s seconds", timeout)
                sleep(timeout)
                self.rate_limit_exceeded = False

        response = super().request(method, url, **kwargs)
        if int(response.headers["X-RateLimit-Remaining"]) <= 0:
            self.rate_limit_exceeded = True
            self.rate_limit_until = time() + int(response.headers["X-RateLimit-Reset"]) + 1
        if response.status_code != 200:
            raise RequestException(response)

        return response

    def get_group(self, urlname: str) -> Response:
        return self.get(f"/{urlname}").json()

    def get_group_events(self, urlname: str) -> Response:
        return self.get(
            f"/{urlname}/events", params={"status": "past", "page": 200}
        ).json()

    def get_event_attendance(self, urlname: str, event_id: int) -> Response:
        return self.get(
            f"/{urlname}/events/{event_id}/attendance", params={"page": 200}
        ).json()
