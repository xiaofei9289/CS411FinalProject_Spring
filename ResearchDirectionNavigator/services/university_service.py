"""University-facing service layer used by W2/W3 and layout dropdowns."""

from dash import html

from components.widget02 import build_university_list_for_widget02
from components.widget03 import make_comparisions_among_universities_for_widget_03
from utils.mysql import (
    w02_get_all_university_names,
    w02_get_university_w2_dashboard,
    w03_get_comparision_information_among_universities,
)


def get_university_dropdown_options():
    university_rows=w02_get_all_university_names()
    return [{"label": row["name"], "value": row["name"]} for row in university_rows]


def get_widget02_university_profile(selected_university):
    if not selected_university:
        return html.P("Please select a university first")
    dashboard=w02_get_university_w2_dashboard(selected_university, keyword_chart_limit=10)
    return build_university_list_for_widget02(dashboard)


def get_widget03_comparison(selected_universities):
    if not selected_universities:
        return html.P("No Items Selected")
    if len(selected_universities)==1:
        return html.P("Please selected at 2 or more universities")
    comparison_rows=w03_get_comparision_information_among_universities(selected_universities)
    return make_comparisions_among_universities_for_widget_03(comparison_rows)
