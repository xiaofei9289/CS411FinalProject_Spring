from dash import html

from components.widget02 import build_university_list_for_widget02
from components.widget03 import make_comparisions_among_universities_for_widget_03
from utils.mysql import (
    w02_get_all_university_names,
    w02_get_university_w2_dashboard,
    w03_get_comparision_information_among_universities,
)

# define a fuction to get all university names and turn them into dropdown options
def get_university_dropdown_options():
    # get all university rows from database/service
    university_rows = w02_get_all_university_names()
    # create an empty list to store dropdown options
    dropdown_options = []
    # iterate each row 
    for row in university_rows:
        # use the university name as both label and value
        option = {
            "label": row["name"],
            "value": row["name"]
        }
        dropdown_options.append(option)
    return dropdown_options

# define a function to show the university profile content for widget 02
def get_widget02_university_profile(selected_university):
    if not selected_university:
        return html.P("Please select a university first")
    dashboard=w02_get_university_w2_dashboard(selected_university, keyword_limit=10)
    return build_university_list_for_widget02(dashboard)

# define a function to show comparison result for widget 03
def get_widget03_comparison(selected_universities):
    if not selected_universities:
        return html.P("No universities selected.")
    # same dedupe rules as w03: strip, skip empty, preserve order (multi-select can repeat the same school)
    unique_names=[]
    for item in selected_universities:
        name=(item or "").strip()
        if not name:
            continue
        if name not in unique_names:
            unique_names.append(name)
    if len(unique_names)<2:
        return html.P("Please select at least two different universities.")
    comparison_rows=w03_get_comparision_information_among_universities(unique_names)
    return make_comparisions_among_universities_for_widget_03(comparison_rows)
