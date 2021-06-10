import pathlib
import urllib.parse
from typing import NamedTuple, List

import bs4
import aiohttp

from dffml import op


class Flight(NamedTuple):
    airline: str
    cost: float


@op(
    imp_enter={
        "session": (
            lambda self: aiohttp.ClientSession(
                trust_env=True,
                cookie_jar=aiohttp.CookieJar(),
                headers={
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "accept-language": "en-US,en;q=0.9",
                    "cache-control": "no-cache",
                    "pragma": "no-cache",
                    "sec-fetch-dest": "document",
                    "sec-fetch-mode": "navigate",
                    "sec-fetch-site": "same-origin",
                    "sec-fetch-user": "?1",
                    "sec-gpc": "1",
                    "upgrade-insecure-requests": "1",
                    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
                },
            )
        ),
    },
)
async def alaskaair_round_trip_html(
    self, src: str, dst: str, leave: str, back: str, adults: int
) -> List[Flight]:
    request_body = urllib.parse.urlencode(
        {
            "flightType": 1,
            "AwardOption": "MilesOnly",
            "DirtyForm": False,
            "IsRoundTrip": True,
            "IsMultiCity": False,
            "RequiresUmnrService": "",
            "ShowOnlyContractFares": False,
            "ShowContractAndAllFares": False,
            "ShopAwardCalendar": False,
            "ShopLowFareCalendar": False,
            "ContractFaresOption": None,
            "DepartureCity1": src,
            "ArrivalCity1": dst,
            "DepartureDate1": leave,
            "ReturnDate": back,
            "AdultCount": f"{adults} adults",
            "ChildrenCount": 0,
            "InfantCount": 0,
            # TODO Change client state code for sales tax I'm guessing. Or don't :P
            "ClientStateCode": "OR",
        }
    )
    self.logger.debug("Request body: %s", request_body)
    async with self.parent.session.post(
        "https://www.alaskaair.com/Shopping/Flights/Shop",
        data=request_body,
        headers={"content-type": "application/x-www-form-urlencoded"},
    ) as response:
        soup = bs4.BeautifulSoup(await response.text(), "html.parser")
        print(soup.prettify())
