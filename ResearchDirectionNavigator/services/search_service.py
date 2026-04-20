from dash import html

from components.widget01 import (
    build_publication_list_for_widget01,
    get_widget01_initial_results_children,
)
from components.widget10 import build_widget10_openalex_results
from utils.mysql import w01_search_papers_based_on_keywords
from utils.openalex import search_openalex_works

# define a function to decide use which search
# use global search text first; if it is empty, use the local widget input
def keyword_search_decision_in_diverse_areas(global_text, local_widget_text):

    input_text_in_global=(global_text or "").strip()
    if input_text_in_global:
        return input_text_in_global
    return (local_widget_text or "").strip()

# define a function to run the search for Widget 1
def run_widget01_search(global_val, w1_value):
    selected_text=keyword_search_decision_in_diverse_areas(global_val, w1_value)
    if not selected_text:
        return get_widget01_initial_results_children()
    # search papers in MySQL
    max_row_limit=100
    w1_publication_rows=w01_search_papers_based_on_keywords(selected_text, limit=max_row_limit)
    return build_publication_list_for_widget01(w1_publication_rows)

# define a functin to build the initial message for Widget 10
def get_widget10_initial_results():
    return html.P(
        "Use OpenAlex Search or Global Search to list works (titles are links).",
        className="text-muted small",
    )

# define a function to run the search for Widget 10
def run_widget10_search(global_text, local_text):
    keyword = keyword_search_decision_in_diverse_areas(global_text, local_text)

    # show the initial message if no keyword is given
    if not keyword:
        return get_widget10_initial_results()

    # search works from OpenAlex
    openalex_works, error_message = search_openalex_works(keyword, per_page=25)

    # build the result table UI
    return build_widget10_openalex_results(
        openalex_works,
        keyword,
        error=error_message,
    )

# define a function to build the feedback message for the global search area
def build_global_search_feedback_children(keyword):
    # do not show anything when the keyword is empty
    if not keyword:
        return ""

    # check whether Widget 1 has at least one result
    paper_rows = w01_search_papers_based_on_keywords(keyword, limit=1)
    # check whether OpenAlex has at least one result
    openalex_works, error_message = search_openalex_works(keyword, per_page=1)
    has_widget01_result = bool(paper_rows)
    has_widget10_result = bool(openalex_works) and not error_message
    # if at least one widget has results
    if has_widget01_result or has_widget10_result:
        return ""
    # when OpenAlex has a request error
    if error_message:
        return ""
    return html.P(
        "There are no results for this keyword. Please check your input or try another keyword.",
        className="global-search-no-results-text mb-0",
    )
