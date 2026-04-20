from dash import html, dcc
import dash_bootstrap_components as dbc

from services.favorite_service import list_favorites

# create a function to construct the professor search result list
def build_widget09_search_results(search_result_rows):
    # check if there is result or not
    if not search_result_rows:
        return html.P(
            "No professor matched your search. Try a different name.",
            className="text-muted small mb-0",
        )
    # create a list to store the search results
    search_result_list_items=[]
    # iterate each row to get the revevant information
    for candidate_professor_row in search_result_rows:
        faculty_id=int(candidate_professor_row["id"])
        professor_display_name=candidate_professor_row.get("faculty_name") or "(no name)"
        university_display_name=candidate_professor_row.get("university_name") or ""
       
       # build the left text block that shows professor name and university name
        professor_info_block = html.Div(
            [
                html.Div(
                    professor_display_name,
                    className="fw-semibold small",
                ),
                html.Div(
                    university_display_name,
                    className="text-muted small",
                ),
            ]
        )
        # build the add button on the right side
        add_button = dbc.Button(
            "+ Add",
            id={"type": "w9-add-fav", "index": faculty_id},
            color="warning",
            outline=True,
            size="sm",
            n_clicks=0,
        )

        # build one list item that contains professor info and the add button
        one_result_item = html.Li(
            dbc.Stack(
                direction="horizontal",
                gap=2,
                className="justify-content-between align-items-start",
                children=[
                    professor_info_block,
                    add_button,
                ],
            ),
            className="small border-bottom py-2",
        )
        # add it in the list
        search_result_list_items.append(one_result_item)

    return html.Ul(search_result_list_items, className="list-unstyled mb-0 small")

# define a function to build the favorite professor list in Widget 9
def build_widget09_favorites_list(favorite_rows):
    # check if exist favorite professor
    if not favorite_rows:
        return html.P(
            "No favorites yet — search a professor above and click '+ Add'.",
            className="text-muted small mb-0",
        )
    # create an empty list to store all favorite items
    favorite_list_items=[]
    # iterate each favorite professor row
    for one_favorite_row in favorite_rows:
        favorite_faculty_id=int(one_favorite_row["faculty_id"])
        professor_display_name=one_favorite_row.get("faculty_name") or f"Faculty {favorite_faculty_id}"
        university_display_name=one_favorite_row.get("university_name") or ""
        
        # build a clickable professor name button
        professor_name_button = dbc.Button(
            professor_display_name,
            id={"type": "w4-open-faculty", "index": favorite_faculty_id},
            color="link",
            className="p-0 text-start fw-semibold small",
            n_clicks=0,
        )

        # build the left text block for the favorite item
        favorite_info_block = html.Div(
            [
                # clickable professor name
                professor_name_button,
                html.Div(
                    university_display_name,
                    className="text-muted small",
                ),
            ]
        )
        # build the remove button on the right side
        remove_button = dbc.Button(
            "×",
            id={"type": "w9-remove-fav", "index": favorite_faculty_id},
            color="danger",
            outline=True,
            size="sm",
            n_clicks=0,
        )
        # build one favorite list item
        one_favorite_item = html.Li(
            dbc.Stack(
                # place the professor info and remove button in one horizontal row
                direction="horizontal",
                gap=2,
                className="justify-content-between align-items-start",
                children=[
                    favorite_info_block,
                    remove_button,
                ],
            ),
            className="small border-bottom py-2",
        )

        # add this item into the favorite list
        favorite_list_items.append(one_favorite_item)

    favorite_count = len(favorite_rows)
    return html.Div(
        [
            html.P(
                f"My Favorites ({favorite_count})",
                className="small fw-semibold mb-1",
            ),
            html.Ul(
                favorite_list_items,
                className="list-unstyled mb-0 small",
            ),
        ]
    )


# define a function to load the initial favorite list when the page first opens
def get_widget09_initial_favorites():
    # read the favorite professor rows from the service layer
    favorite_rows = list_favorites()

    # build and return the favorite list UI
    return build_widget09_favorites_list(favorite_rows)

# define a function to builds the layout of Widget 09 in the dashboard
# the column for widget 9 is about the favorite professors.
def build_column_widget09():
    return dbc.Col(
        children=[
            html.Div(
                className="section-label-row",
                children=[
                    html.Span(
                        "SAVE & EDIT INTERESTED PROFESSORS",
                        className="section-label section-label-network",
                    )
                ],
            ),
            html.Div(
                className="widget-card accent-yellow",
                children=[
                    html.Div(
                        className="widget-title-row",
                        children=[
                            html.Span("W9", className="widget-tag"),
                            html.Span(
                                "Favorite Professors",
                                className="widget-title",
                            ),
                            html.Span("MySQL", className="tech-badge mysql"),
                            html.Span(
                                "Transaction",
                                className="tech-badge transaction",
                            ),
                            html.Span(
                                "Constraint",
                                className="tech-badge constraint",
                            ),
                        ],
                    ),
                    html.P(
                        "Save and manage professors you're interested in.",
                        className="widget-subtitle",
                    ),
                    html.P(
                        "Examples: Chris Manning, Robert Schapire...",
                        className="text-muted small mb-2",
                    ),
                    html.Label(
                        className="widget-search-inline search-row-focus",
                        children=[
                            dcc.Input(
                                id="search_widget09",
                                type="text",
                                placeholder="Enter faculty name to search",
                                className="form-control",
                                debounce=True,
                            ),
                            dbc.Button(
                                "Explore",
                                id="search_widget09_button",
                                color="secondary",
                                size="sm",
                                className="button-search-accent-yellow",
                                n_clicks=0,
                            ),
                        ],
                    ),
                    html.Div(
                        id="widget_09_search_results",
                        className="mb-2",
                        children=[
                            html.P(
                                "Type a name and click Explore to find candidates to favorite.",
                                className="text-muted small mb-0",
                            ),
                        ],
                    ),
                    html.Hr(className="my-2"),
                    html.Div(
                        id="widget_09_favorites",
                        children=get_widget09_initial_favorites(),
                    ),
                ],
            ),
        ],
        xs=12,
        sm=12,
        md=4,
        className="py-2",
    )