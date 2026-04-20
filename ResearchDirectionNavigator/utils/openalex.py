import json
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from dotenv import load_dotenv

# find the project root folder
project_root = Path(__file__).resolve().parent.parent

# load environment variables from .env
load_dotenv(project_root / ".env")

# OpenAlex API url
OPENALEX_WORKS_URL = "https://api.openalex.org/works"


# convert a value to int if possible, otherwise return default value
def safe_int(value, default_value):
    if value is None:
        return default_value
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        cleaned_value = value.strip()
        if cleaned_value.isdigit():
            return int(cleaned_value)
    return default_value


def search_openalex_works(search_text, per_page=25):

    # clean the input text
    cleaned_text = str(search_text).strip()
    if cleaned_text == "":
        return [], "empty query"
    per_page = safe_int(per_page, 25)
    if per_page < 1:
        per_page = 1
    if per_page > 200:
        per_page = 200

    # build query parameters
    params = {
        "search": cleaned_text,
        "per_page": per_page
    }

    # add mailto if it exists in .env
    mailto_value = os.getenv("OPENALEX_MAILTO", "").strip()
    if mailto_value != "":
        params["mailto"] = mailto_value

    # build final request url
    final_url = OPENALEX_WORKS_URL + "?" + urllib.parse.urlencode(params)

    # create request object
    request = urllib.request.Request(
        final_url,
        headers={
            "User-Agent": "CS411-ResearchDirectionNavigator/1.0 (course project)"
        }
    )

    # send request — failures become ([], error_message) so Dash callbacks stay stable
    try:
        with urllib.request.urlopen(request, timeout=35) as response:
            response_text = response.read().decode("utf-8")
        data = json.loads(response_text)
    except urllib.error.HTTPError as e:
        return [], f"OpenAlex HTTP {e.code}: {e.reason}"
    except urllib.error.URLError as e:
        reason = e.reason
        if isinstance(reason, BaseException):
            reason = str(reason)
        return [], f"OpenAlex request failed: {reason}"
    except json.JSONDecodeError:
        return [], "OpenAlex returned invalid JSON"
    except UnicodeDecodeError:
        return [], "OpenAlex response could not be decoded as UTF-8"

    if not isinstance(data, dict):
        return [], "OpenAlex returned an unexpected JSON shape"

    # get result list from API response
    works = data.get("results", [])
    if not isinstance(works, list):
        works = []

    result_list = []

    # loop through each work
    for work in works:
        if not isinstance(work, dict):
            continue
        # get title
        title = work.get("display_name")
        if not title:
            title = work.get("title")
        if not title:
            title = "—"
        title = str(title).strip()

        # limit title length
        if len(title) > 500:
            title = title[:500]

        # get publication year
        year_value = safe_int(work.get("publication_year"), None)

        # get citation count
        cited_count_value = safe_int(work.get("cited_by_count"), 0)

        # get work url
        work_url = work.get("id", "")

        # get author names
        author_name_list = []
        authorships = work.get("authorships", [])
        if not isinstance(authorships, list):
            authorships = []

        for authorship in authorships[:5]:
            if not isinstance(authorship, dict):
                continue
            author_info = authorship.get("author", {})
            if not isinstance(author_info, dict):
                author_info = {}
            author_name = str(author_info.get("display_name", "")).strip()
            if author_name != "":
                author_name_list.append(author_name)

        # combine first 3 author names
        authors_short = ", ".join(author_name_list[:3])
        if len(author_name_list) > 3:
            authors_short = authors_short + ", …"
        if authors_short == "":
            authors_short = "—"

        # save one work record
        one_work = {
            "title": title,
            "year": year_value,
            "cited_by_count": cited_count_value,
            "authors_short": authors_short,
            "url": work_url,
        }

        result_list.append(one_work)

    return result_list, None