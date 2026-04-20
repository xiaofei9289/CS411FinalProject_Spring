"""Keyword resolution, publication search (W1), OpenAlex search (W10), global empty-state hint."""

from dash import html

from components.widget01 import (
    build_publication_list_for_widget01,
    get_widget01_initial_results_children,
)
from components.widget10 import build_widget10_openalex_results
from utils.mysql import w01_search_papers_based_on_keywords
from utils.openalex import search_openalex_works


def keyword_search_decision_in_diverse_areas(global_text, local_widget_text):
    """Prefer Global Search when set; otherwise use the widget's local input."""
    input_text_in_global=(global_text or "").strip()
    if input_text_in_global:
        return input_text_in_global
    return (local_widget_text or "").strip()


def run_widget01_search(global_val, w1_value):
    selected_text=keyword_search_decision_in_diverse_areas(global_val, w1_value)
    if not selected_text:
        return get_widget01_initial_results_children()
    max_row_limit=100
    w1_publication_rows=w01_search_papers_based_on_keywords(selected_text, limit=max_row_limit)
    return build_publication_list_for_widget01(w1_publication_rows)


def widget10_initial_results_children():
    return html.P(
        "Use OpenAlex Search or Global Search to list works (titles are links).",
        className="text-muted small",
    )


def run_widget10_search(global_val, local_input_text):
    selected_text=keyword_search_decision_in_diverse_areas(global_val, local_input_text)
    if not selected_text:
        return widget10_initial_results_children()
    works, err=search_openalex_works(selected_text, per_page=25)
    return build_widget10_openalex_results(works, selected_text, error=err)


def build_global_search_feedback_children(keyword):
    """Return children for global_search_feedback when Explore is clicked and keyword is non-empty."""
    if not keyword:
        return ""
    rows=w01_search_papers_based_on_keywords(keyword, limit=1)
    works, err=search_openalex_works(keyword, per_page=1)
    has_w1=bool(rows)
    has_w10=bool(works) and not err
    if has_w1 or has_w10:
        return ""
    if err:
        return ""
    return html.P(
        "There's no results about your input keyword, please check the input or change another keyword.",
        className="global-search-no-results-text mb-0",
    )
