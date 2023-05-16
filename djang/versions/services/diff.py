import requests
from ..models import Revision
import re
import diff_match_patch as dmp_module
from html import escape as html_escape
from django.utils.html import format_html

from . import bot


def get_content(revision: Revision) -> str:
    revision_id = revision.wiki_rev_id
    # 'https://he.wikisource.org/w/api.php?action=query&prop=revisions&revids=1416783&rvprop=ids|content&format=json'
    response = requests.get(
        "https://he.wikisource.org/w/api.php",
        params={
            "action": "query",
            "prop": "revisions",
            "revids": str(revision_id),
            "rvprop": "ids|content",
            "format": "json",
        },
    )
    data = response.json()
    pages = data["query"]["pages"]
    # force a single page
    (page,) = list(pages.values())
    # force a single revision
    (revision,) = page["revisions"]
    assert revision["revid"] == revision_id
    return revision["*"]


def sanitize_text(inp: str) -> str:
    replacements = {
        "־–—‒―": "-",
        "&para;": "",
    }
    for k, v in replacements.items():
        inp = re.sub(k, v, inp)
    return inp


def ugly_tag(tag_name, inner_text):
    """
    Adds the tag twice, once escaped and once not, to allow both visual readers to see the tag,
    and for CSS formatting
    """
    tag_raw = f"<{tag_name}>"
    tag_end_raw = f"</{tag_name}>"
    inner1 = f"{tag_raw}{inner_text}{tag_end_raw}"
    inner2 = html_escape(inner1)
    inner3 = f"{tag_raw}{inner2}{tag_end_raw}"
    return inner3
    return format_html(
        f"<{tag_name}>{{}}</{tag_name}>", f"<{tag_name}>{inner_text}</{tag_name}>"
    )


def ugly_diff_match_html(content_a: str, content_b: str) -> str:
    dmp = dmp_module.diff_match_patch()
    diffs = dmp.diff_main(content_a, content_b)
    html = []
    for op, data in diffs:
        text = data
        if op == dmp.DIFF_INSERT:
            html.append(ugly_tag("ins", text))
        elif op == dmp.DIFF_DELETE:
            html.append(ugly_tag("del", text))
        elif op == dmp.DIFF_EQUAL:
            html.append(text)
    return "".join(html)


def post_processing(ugly_html, formatting_style) -> str:
    # TODO move here?
    return bot.post_processing(ugly_html, formatting_style)


def diff(revision_a: Revision, revision_b: Revision, style: str) -> str:
    content_a = get_content(revision_a)
    content_b = get_content(revision_b)
    ugly_html = ugly_diff_match_html(content_a, content_b)
    processed = post_processing(ugly_html, style)

    return processed
