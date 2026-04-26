from dash import html, dcc
import dash_bootstrap_components as dbc

from components.header import (
    build_top_navigation_bar,
    build_title_and_search_section,
    build_page_footer_section,
)
from components.widget01 import build_column_widget01
from components.widget02 import build_column_widget02
from components.widget03 import build_column_widget03
from components.widget04 import create_layout_for_widget04
from components.widget05 import build_column_widget05
from components.widget06 import build_column_widget06
from components.widget07 import build_column_widget07
from components.widget08 import build_column_widget08
from components.widget09 import build_column_widget09
from components.widget10 import build_column_widget10
from services.search_service import get_widget10_initial_results
from services.trend_service import widget05_initial_results_children
from services.university_service import get_university_dropdown_options

"""
this function is responsible for building the main layout of the dashboard, which includes a header, 
a sidebar for navigation, and a main content area where different pages will be displayed based on user interaction. 
it constructs the middle area of the page, including multiple columns and rows, to organize the content effectively.
each widge t is placed within a specific column and row to ensure a clean and responsive design.

the layout is:

# Row 1 W1 Keyword Publication Search        |  W8 Related Keywords
# Row 2 W2 University Profile                |  W3 University Comparison
# Row 3 W7 Collaboration Network             |  W9 Favorite Professors            | W10 OpenAlex
# Row 4 W5 Research Trends                   |  W6 Faculty Recommendation

"""
# construct a function for the main layout 
def build_dashboard_layout():
    # the first row contains widget 1 and widget 8
    # the widge 1 is placed in the first column and the widget 8 is placed in the second column
    column_for_widget01=build_column_widget01()
    # the column for widget 8 is about the paper list and it accounts for half of the width of the page
    column_for_widget08=build_column_widget08()

    # place the two columns in the first row
    first_row_for_widget01_and_widget08=dbc.Row(
        children=[ column_for_widget01, column_for_widget08],
        className="g-3",
    )
    
    # the second row contains widget 2 and widget 3
    # the widget 2 is placed in the first column and the widget 3 is placed in the second column
    # load university list for W2 dropdown only. W3 loads the same list again below so each widget block stays self-contained 
    dropdown_options_for_widget02_and_widget03=get_university_dropdown_options()

    column_for_widget02=build_column_widget02(dropdown_options_for_widget02_and_widget03)
    column_for_widget03=build_column_widget03(dropdown_options_for_widget02_and_widget03)

    # place the two columns in the second row
    second_row_for_widget02_and_widget03=dbc.Row(
        children=[column_for_widget02, column_for_widget03],
        className="g-3",
    )

    # the third row contains widget 7, widget 9, widget 10
    # the widge 7 is placed in the first column
    column_for_widget07=build_column_widget07()
    # the widget 9 is placed in the second column
    column_for_widget09=build_column_widget09()
    # the widget 10 is placed in the third column
    column_for_widget10=build_column_widget10(get_widget10_initial_results())

    # place the three columns in the third row
    third_row_for_widget07_and_widget09_and_widget10=dbc.Row(
        children=[column_for_widget07, column_for_widget09, column_for_widget10],
        className="g-3",
    )

    # the fourth row contains widget 5 and widget 6
    # the widget 5 is placed in the first column and the widget 6 is placed in the second column
    column_for_widget05=build_column_widget05(widget05_initial_results_children())
    # the column for widget 6 is about the smart faculty recommendation
    column_for_widget06=build_column_widget06()
    # place the two column in the fourth row
    fourth_row_for_widget05_and_widget06=dbc.Row(
        children=[column_for_widget05, column_for_widget06],
        className="g-3",
    )   

    # place all the rows in the main content area
    main_container_area_for_all_rows=dbc.Container(
        children=[
            first_row_for_widget01_and_widget08,
            second_row_for_widget02_and_widget03,
            third_row_for_widget07_and_widget09_and_widget10,
            fourth_row_for_widget05_and_widget06,
        ],
        fluid=True,
        className="dashboard-main py-3"
    )  
    # return the main content area to be used in the overall layout of the dashboard
    return main_container_area_for_all_rows

# create a function to build the full layout
def build_full_app_layout():
    # build the main visible sections of the page
    page_sections=[
        build_top_navigation_bar(),
        build_title_and_search_section(),
        build_dashboard_layout(),
        build_page_footer_section(),
    ]
    # build Widget 04 extra components
    widget04_store, widget04_off_canvas_bar=create_layout_for_widget04()
    # create a hidden placeholder button for Widget 04 pattern-matching callbacks
    w4_pattern_placeholder=html.Div(
        [
            dbc.Button(
                id={"type": "w4-open-faculty", "index": -999999},
                n_clicks=0,
                style={"display": "none"},
                title="",
            )
        ],
        style={"display": "none"},
    )
    # create hidden placeholder buttons for Widget 09 pattern-matching callbacks
    w9_pattern_placeholder=html.Div(
        [
            dbc.Button(
                id={"type": "w9-add-fav", "index": -999999},
                n_clicks=0,
                style={"display": "none"},
            ),
            dbc.Button(
                id={"type": "w9-remove-fav", "index": -999999},
                n_clicks=0,
                style={"display": "none"},
            ),
        ],
        style={"display": "none"},
    )
    # create hidden placeholder controls for Widget 08 pattern-matching callbacks
    w8_pattern_placeholder=html.Div(
        [
            dbc.Button(
                id={"type": "w8-add-pub", "index": "__placeholder__"},
                n_clicks=0,
                style={"display": "none"},
            ),
            dbc.Button(
                id={"type": "w8-remove-pub", "index": "__placeholder__"},
                n_clicks=0,
                style={"display": "none"},
            ),
            dbc.Button(
                id={"type": "w8-update-pub", "index": "__placeholder__"},
                n_clicks=0,
                style={"display": "none"},
            ),
            dcc.Textarea(
                id={"type": "w8-note", "index": "__placeholder__"},
                value="",
                style={"display": "none"},
            ),
            dcc.Dropdown(
                id={"type": "w8-status", "index": "__placeholder__"},
                options=[],
                value=None,
                style={"display": "none"},
            ),
        ],
        style={"display": "none"},
    )
    return html.Div(
        children=[
            html.Div(children=page_sections),
            widget04_store,
            widget04_off_canvas_bar,
            w4_pattern_placeholder,
            w8_pattern_placeholder,
            w9_pattern_placeholder,
        ],
        className="app-container",
    )
