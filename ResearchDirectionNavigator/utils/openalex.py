import json
import os
import urllib.parse
import urllib.request
from pathlib import Path

from dotenv import load_dotenv

# find the project root folder
project_root=Path(__file__).resolve().parent.parent

# load environment variables from .env
load_dotenv(project_root / ".env")

# OpenAlex API url
OPENALEX_WORKS_URL="https://api.openalex.org/works"


def search_openalex_works(search_text, per_page=25):

    # clean the input text
    cleaned_text=str(search_text).strip()
    if cleaned_text=="":
        return [], "empty query"
    if str(per_page).isdigit():
        per_page=int(per_page)
    else:
        per_page=25

    # build query parameters
    params={
        "search": cleaned_text,
        "per_page": per_page
    }

    # add mailto if it exists in .env
    mailto_value=os.getenv("OPENALEX_MAILTO", "").strip()
    if mailto_value!="":
        params["mailto"]=mailto_value

    # build final request url
    final_url=OPENALEX_WORKS_URL + "?" + urllib.parse.urlencode(params)

    # create request object
    request=urllib.request.Request(
        final_url,
        headers={
            "User-Agent": "CS411-ResearchDirectionNavigator/1.0 (course project)"
        }
    )

    # send request to OpenAlex
    with urllib.request.urlopen(request, timeout=35) as response:
        response_text=response.read().decode("utf-8")
    data=json.loads(response_text)

    # get result list from API response
    works=data.get("results", [])

    result_list=[]

    # loop through each work
    for work in works:
        # get title
        title=work.get("display_name")
        if not title:
            title=work.get("title")
        if not title:
            title="—"
        title=str(title).strip()

        # limit title length
        if len(title)>500:
            title=title[:500]

        # get publication year
        year_value=work.get("publication_year")

        # get citation count
        cited_count=work.get("cited_by_count")
        if str(cited_count).isdigit():
            cited_count_value=int(cited_count)
        else:
            cited_count_value=0

        # get work url
        work_url=work.get("id", "")

        # get author names
        author_name_list=[]
        authorships=work.get("authorships", [])

        for authorship in authorships[:5]:
            author_info=authorship.get("author", {})
            author_name=str(author_info.get("display_name", "")).strip()
            if author_name!="":
                author_name_list.append(author_name)

        # combine first 3 author names
        authors_short=", ".join(author_name_list[:3])
        if len(author_name_list)>3:
            authors_short=authors_short + ", …"
        if authors_short=="":
            authors_short="—"

        # save one work record
        one_work={
            "title": title,
            "year": year_value,
            "cited_by_count": cited_count_value,
            "authors_short": authors_short,
            "url": work_url,
        }

        result_list.append(one_work)

    return result_list, None