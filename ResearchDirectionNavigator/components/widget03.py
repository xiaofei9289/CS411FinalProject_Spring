from dash import html, dcc
import dash_bootstrap_components as dbc

# create a function to covert the query information into a Dash component
def make_comparisions_among_universities_for_widget_03(rows):
    # check if there's data or not
    # if no data
    if rows is None:
        message_for_None=html.P("No Data, No Results Searching")
        return message_for_None
    # check if the data in the list is >=2
    # get the number of rows
    number_of_rows=len(rows)
    if number_of_rows<2:
        message_for_list=html.P("Please Selected At Least 2 Or More Universities")
        return message_for_list
    
    # create the header row of the table
    header_row=html.Tr([
        html.Th("University Name"),
        html.Th("Total Publications"),
        html.Th("Faculty Number"),
        html.Th("Publications in Past 20 Years"),
        html.Th("Total Citations"),
    ])

    # create a list to store all data rows
    list_of_data_rows=[]
    # iterate each university result
    for row in rows:
        one_row=html.Tr([
            html.Td(row.get("university_name", "")),
            html.Td(row.get("total_publication_count", "")),
            html.Td(row.get("faculty_number", "")),
            html.Td(row.get("publication_count_last_twenty_years", "")),
            html.Td(row.get("total_citation_sum", "")),
        ])
        list_of_data_rows.append(one_row)


    # create the table
    table=html.Table(
        children=[header_row]+list_of_data_rows,
        className="table table-sm table-bordered",
        style={"backgroundColor": "#e8f5e9"},
    )

    # create an outer container for the table so that we can add a border frame
    table_with_frame=html.Div(
        table,
        style={
            "border": "2px solid #3d6b5c",
            "borderRadius": "6px",
            "overflow": "hidden",
            "width": "100%",
        },
    )
    return html.Div([
        html.H5("University Comparison Results"),
        table_with_frame,
    ])


# the column for widget 3 is about the university comparison
# same source as W2: options for the multi-select comparison dropdown (independent variable name for W3).
def build_column_widget03(dropdown_options):
    return dbc.Col(
        children=[
            html.Div(
                className="section-label-row",
                children=[
                    html.Span(
                        "UNIVERSITY COMPARISIONS",
                        className="section-label section-label-university",
                    )
                ],
            ),
            html.Div(
                className="widget-card accent-purple",
                children=[
                    html.Div(
                        className="widget-title-row",
                        children=[
                            html.Span("W3", className="widget-tag"),
                            html.Span(
                                "Universities' Comparision",
                                className="widget-title",
                            ),
                            html.Span("MySQL", className="tech-badge mysql"),
                            html.Span("View", className="tech-badge view"),
                        ],
                    ),
                    html.P(
                        "Compare research output across multiple institutions.",
                        className="widget-subtitle",
                    ),
                    html.Label(
                        className="widget-search-inline search-row-focus",
                        children=[
                            html.Div(
                                className="flex-grow-1",
                                children=[
                                    dcc.Dropdown(
                                        id="widget_03_university_dropdown",
                                        options=dropdown_options,
                                        placeholder="Pick at least 2 or more universities",
                                        clearable=True,
                                        searchable=True,
                                        multi=True,
                                    ),
                                ],
                            ),
                            dbc.Button(
                                "Make Comparision",
                                id="search_widget03_button",
                                color="secondary",
                                size="sm",
                                className="button-search-accent-purple",
                                n_clicks=0,
                            ),
                        ],
                    ),
                    html.Div(
                        id="widget_03_results",
                        children=[
                            html.P(
                                "This area will display the comparison information among the selected universities, and it will show as a table."
                            ),
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
