from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px

# create a function to get dark-to-light RGB colors for bars to form a smooth gradient
def gradient_bar_colors(number_of_bars):
    # define the start color (dark blue) and end color (light green)
    rgb_dark=(44, 81, 110)
    rgb_light=(209, 234, 229)
    # return an empty list if there are no bars
    if number_of_bars<=0:
        return []
    # if there is only one bar, use the dark color only
    if number_of_bars==1:
        return [f"rgb({rgb_dark[0]},{rgb_dark[1]},{rgb_dark[2]})"]
    # create a list to store the gradient colors
    gradient_colors=[]
    # generate one color for each bar
    for i in range(number_of_bars):
        blend=i/(number_of_bars-1)
        red=int(rgb_dark[0]+(rgb_light[0]-rgb_dark[0])*blend)
        green=int(rgb_dark[1]+(rgb_light[1]-rgb_dark[1])*blend)
        blue=int(rgb_dark[2]+(rgb_light[2]-rgb_dark[2])*blend)
        gradient_colors.append(f"rgb({red},{green},{blue})")
    return gradient_colors


# create a function to convert the query information into a Dash component
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

    # create three small cards in one horizontal strip
    summary_cards=dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("Total Publications"),
            html.H4(str(total_publications))
        ]), style={"backgroundColor": summary_card_backgrounds[0]}), md=4),

        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("Major Research Area"),
            html.P(primary_research_area)
        ]), style={"backgroundColor": summary_card_backgrounds[1]}), md=4),

        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("Number of Faculty"),
            html.H4(str(faculty_count))
        ]), style={"backgroundColor": summary_card_backgrounds[2]}), md=4),
    ])

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
        keyword_bar_colors=gradient_bar_colors(len(keyword_labels))
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


# the column for widget 2 is about the university research profile
def build_column_widget02(dropdown_options):
    return dbc.Col(
        children=[
            html.Div(
                className="section-label-row",
                children=[
                    html.Span(
                        "UNIVERSITY ANALYSIS",
                        className="section-label section-label-university",
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