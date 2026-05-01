from dash import html,dcc
import dash_bootstrap_components as dbc

# top navigation bar
def build_top_navigation_bar():
    navigation_bar=html.Div(className="top-navigation-bar", children=[
    # left part
    html.Div(className="app-brand", children=[
        # brand name
        html.Div("AcademicExplorer", className="app-brand-name"),
        # brand tag
        html.Div("Find Your Research Direction & resources",
                 className="app-brand-tag"),
    ]),
    # right part
    html.Div(className="nav-right", children=[html.Span("👤")]),
    ])
    # return the finished navigation bar
    return navigation_bar


# title section + global search box
def build_title_and_search_section():
    all_contents=html.Div(className="title-section", children=[
        # main title
        html.H1("Explore&Discover&Connect.", className="hero-title"),
        # sub-title
        html.P("Explore research directions, professors, universities, and scholarly trends in this dashboard.",
               className="hero-subtitle"),
        # global search
        html.Div(className="global-search-block", children=[
            html.Div(className="global-search-heading", children=[
                html.Span("Global Search", className="global-search-badge"),
                html.Span(
                    "Begin your exploration with a Keyword",
                    className="global-search-hint",
                ),
            ]),
            html.Label(
                className="global-search-input-row search-row-focus",
                children=[
                    dcc.Input(
                        id="global_search_input",
                        type="text",
                        placeholder=(
                            "e.g., NLP, LLM …"
                        ),
                        className="form-control global-search-input",
                        debounce=True,
                    ),
                    dbc.Button(
                        "Explore",
                        id="global_search_button",
                        color="secondary",
                        className="global-search-button button-search-accent-blue",
                    ),
                ],
            ),
            html.Div(id="global_search_feedback", className="global-search-feedback"),
        ]),
    ])
    return all_contents

# footer with course / project / tech info
def build_page_footer_section():
    area_for_footer=html.Footer(
        className="app-footer border-top py-3 mt-3 text-muted text-center",
        children=[
            html.Div("Project: Academic Research Direction Explorer"),
            html.Div("Stack: MySQL · MongoDB · Neo4j · OpenAlex"),
            html.Div("Team: Xiaofei Feng · Yuxin Zhang"),
            html.Div("Course: CS411 Database Systems · Spring 2026"),
        ],
    )
    return area_for_footer