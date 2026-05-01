from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px

from utils.common import make_gradient_colors


# university info UI
def build_university_list_for_widget02(university_data):
    # check if the input is empyt
    if university_data is None or len(university_data)==0:
        return html.P("No university found for this research. Please input another university name")
    # extracr the relevant information from 
    university_name=university_data.get("university_name", "")
    total_publications=int(university_data.get("total_publications") or 0)
    faculty_count=int(university_data.get("faculty_count") or 0)
    primary_research_area=university_data.get("major_research_area") or "—"
    keyword_stats=university_data.get("keywords") or []

    # three distinct light backgrounds 
    summary_card_backgrounds=("#e3ecf4", "#e5f2ee", "#f4efe8")

    # create three small cards
    summary_cards=dbc.Row(
        [
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H6("Total Publications"),
                            html.H4(str(total_publications)),
                        ],
                        className="h-100 d-flex flex-column justify-content-center",
                    ),
                    className="h-100 border-0",
                    style={"backgroundColor": summary_card_backgrounds[0]},
                ),
                md=4,
                className="d-flex",
            ),
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H6("Major Research Area"),
                            html.P(primary_research_area, className="mb-0"),
                        ],
                        className="h-100 d-flex flex-column justify-content-center",
                    ),
                    className="h-100 border-0",
                    style={"backgroundColor": summary_card_backgrounds[1]},
                ),
                md=4,
                className="d-flex",
            ),
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H6("Number of Faculty"),
                            html.H4(str(faculty_count)),
                        ],
                        className="h-100 d-flex flex-column justify-content-center",
                    ),
                    className="h-100 border-0",
                    style={"backgroundColor": summary_card_backgrounds[2]},
                ),
                md=4,
                className="d-flex",
            ),
        ],
        className="g-3 align-items-stretch mb-3",
    )

    # build chart
    # check if it is empty
    if len(keyword_stats)==0:
        chart=html.P("No keyword data available")
    else:
        # if not empty, create two list to store keyword names and publication counts
        keyword_labels=[]
        publication_counts=[]
        # iterate every keyword record and collect the keyword name and publication count
        for row in keyword_stats:
            keyword_labels.append(row.get("keyword_name", ""))
            publication_counts.append(row.get("pub_count", 0))
        # generate color for the bars based on the number of keywords
        keyword_bar_colors=make_gradient_colors(len(keyword_labels))
        # create a bar chart 
        keyword_bar_figure=px.bar(
            x=keyword_labels,
            y=publication_counts,
            labels={"x": "Keyword", "y": "Publication count"},
        )
        keyword_bar_figure.update_traces(marker_color=keyword_bar_colors)
        # convert the Plotly figure into a Dash graph component
        chart=dcc.Graph(figure=keyword_bar_figure)

    return html.Div([
        html.H5(university_name),
        summary_cards,
        chart
    ])

# W2 column layout
def build_column_widget02(dropdown_options):
    return dbc.Col(
        children=[
            html.Div(
                className="section-label-row",
                children=[
                    html.Span(
                        "UNIVERSITY ANALYSIS",
                        className="section-label section-label-teal",
                    )
                ],
            ),
            html.Div(
                className="widget-card accent-teal",
                children=[
                    html.Div(
                        className="widget-title-row",
                        children=[
                            html.Span("W2", className="widget-tag"),
                            html.Span(
                                "University Research Profile",
                                className="widget-title",
                            ),
                            html.Span("MySQL", className="tech-badge mysql"),
                            html.Span("View", className="tech-badge view"),
                        ],
                    ),
                    html.P(
                        "View a university's research profile and publication footprint.",
                        className="widget-subtitle",
                    ),
                    html.Label(
                        className="widget-search-inline search-row-focus w2-search-row",
                        children=[
                            html.Div(
                                className="flex-grow-1 w2-dropdown-wrap",
                                children=[
                                    dcc.Dropdown(
                                        id="widget_02_university_dropdown",
                                        options=dropdown_options,
                                        placeholder="Select one to get relevant information",
                                        clearable=True,
                                        searchable=True,
                                        style={"width": "100%"},
                                    ),
                                ],
                            ),
                            dbc.Button(
                                "Show University Details",
                                id="widget_02_view_profile_button",
                                color="secondary",
                                size="sm",
                                className="button-search-accent-teal",
                                n_clicks=0,
                            ),
                        ],
                    ),
                    html.Div(
                        id="widget_02_results",
                        children=[
                            html.P(
                                "This area will display the selected university's relevant information, including publications, faculty, citations and so on.",
                            )
                        ],
                    ),
                ],
            ),
        ],
        xs=12,
        sm=12,
        md=6,
        className="py-2",
    )