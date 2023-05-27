import requests
from typing import NamedTuple, Iterator
from datetime import datetime


class PageResult(NamedTuple):
    title: str
    page_id: int


class RevisionResult(NamedTuple):
    id: int
    timestamp: datetime
    comment: str
    content: str


def get_pages_in_category(cont_dict=None) -> Iterator[PageResult]:
    params = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": "קטגוריה:בוט חוקים",
        "cmnamespace": "0",
        "format": "json",
    }
    if cont_dict:
        params.update(cont_dict)
    response = requests.get(
        "https://he.wikisource.org/w/api.php",
        params=params,
    )
    response.raise_for_status()
    j = response.json()
    results = j["query"]["categorymembers"]
    yield from (PageResult(title=r["title"], page_id=r["pageid"]) for r in results)
    if "continue" in j and "continue" in j["continue"]:
        cont_dict = j["continue"]
        cont_dict.pop("continue")
        yield from get_pages_in_category(cont_dict)


def get_page(title=None, cont_dict=None) -> PageResult:
    params = {
        "action": "query",
        "titles": title,
        "format": "json",
    }
    response = requests.get(
        "https://he.wikisource.org/w/api.php",
        params=params,
    )
    response.raise_for_status()
    j = response.json()
    (page,) = j["query"]["pages"].values()
    return PageResult(title=page["title"], page_id=page["pageid"])


def get_revisions_for_page(page_title: str, cont_dict=None) -> Iterator[RevisionResult]:
    # api.php?action=query&prop=revisions&titles=AntiSpoof&formatversion=2&redirects=1 [try in ApiSandbox]
    params = {
        "action": "query",
        "prop": "revisions",
        "titles": page_title,
        "formatversion": 2,
        "format": "json",
        "rvprop": "timestamp|comment|content|ids",
        "rvslots": "main",
        "rvlimit": "max",
    }
    if cont_dict:
        params.update(cont_dict)
    response = requests.get(
        "https://he.wikisource.org/w/api.php",
        params=params,
    )
    response.raise_for_status()
    j = response.json()
    (page,) = j["query"]["pages"]
    yield from (
        RevisionResult(
            id=int(r["revid"]),
            # supporting Z is only in Python 3.11+
            timestamp=datetime.fromisoformat(r["timestamp"].replace('Z', '+00:00')),
            comment=r["comment"],
            content=r["slots"]["main"]["content"],
        )
        for r in page["revisions"]
    )
    if "continue" in j and "continue" in j["continue"]:
        cont_dict = j["continue"]
        cont_dict.pop("continue")
        yield from get_revisions_for_page(page_title, cont_dict)


import itertools


def bla():
    """
    pages = itertools.islice(get_pages_in_category(), 10)
    for page in pages:
        [print(r) for r in get_revisions_for_page(page.title)]
    """
    [
        print(r.id)
        for r in get_revisions_for_page(
            "חוק איסור פרסומת והגבלת השיווק של מוצרי טבק ועישון"
        )
    ]
