from dash import html, dcc
import dash_bootstrap_components as dbc

from services.publication_favorite_service import list_favorite_publications


W8_STATUS_OPTIONS=[
    {"label": "To Read", "value": "To Read"},
    {"label": "Reading", "value": "Reading"},
    {"label": "Read", "value": "Read"},
]


def get_widget08_initial_results_children():
    return [
        html.P(
            "Search publications above, then click '+ Save' to add papers to your favorites.",
            className="text-muted small mb-0",
        ),
    ]


def build_widget08_search_results(publication_rows):
    if not publication_rows:
        return html.P(
            "No publications matched your search. Try a title or research keyword.",
            className="text-muted small mb-0",
        )
    result_items=[]
    for publication_row in publication_rows:
        publication_id=str(publication_row["publication_id"])
        title=publication_row.get("title") or "(no title)"
        year=publication_row.get("year") or "—"
        venue=publication_row.get("venue") or "—"
        citations=publication_row.get("num_citations") or 0
        keywords=", ".join(publication_row.get("keywords") or [])
        save_button=dbc.Button(
            "+ Save",
            id={"type": "w8-add-pub", "index": publication_id},
            color="warning",
            outline=True,
            size="sm",
            n_clicks=0,
        )
        result_items.append(
            html.Li(
                dbc.Stack(
                    direction="horizontal",
                    gap=2,
                    className="justify-content-between align-items-start",
                    children=[
                        html.Div(
                            [
                                html.Div(title, className="fw-semibold small"),
                                html.Div(
                                    f"{year} · {venue} · {citations} citations",
                                    className="text-muted small",
                                ),
                                html.Div(keywords, className="text-muted small"),
                            ],
                            className="me-2",
                        ),
                        save_button,
                    ],
                ),
                className="small border-bottom py-2",
            )
        )
    return html.Ul(result_items, className="list-unstyled mb-0 small")


def build_widget08_favorites_list(favorite_rows):
    if not favorite_rows:
        return html.P(
            "No favorite publications yet.",
            className="text-muted small mb-0",
        )
    favorite_items=[]
    for favorite_row in favorite_rows:
        publication_id=str(favorite_row["publication_id"])
        title=favorite_row.get("title") or "(no title)"
        year=favorite_row.get("year") or "—"
        venue=favorite_row.get("venue") or "—"
        status=favorite_row.get("status") or "To Read"
        note=favorite_row.get("note") or ""
        favorite_items.append(
            html.Li(
                [
                    dbc.Stack(
                        direction="horizontal",
                        gap=2,
                        className="justify-content-between align-items-start",
                        children=[
                            html.Div(
                                [
                                    html.Div(title, className="fw-semibold small"),
                                    html.Div(f"{year} · {venue}", className="text-muted small"),
                                ]
                            ),
                            dbc.Button(
                                "×",
                                id={"type": "w8-remove-pub", "index": publication_id},
                                color="danger",
                                outline=True,
                                size="sm",
                                n_clicks=0,
                            ),
                        ],
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.Dropdown(
                                    id={"type": "w8-status", "index": publication_id},
                                    options=W8_STATUS_OPTIONS,
                                    value=status,
                                    clearable=False,
                                    className="small",
                                ),
                                xs=12,
                                md=4,
                                className="mt-2",
                            ),
                            dbc.Col(
                                dcc.Textarea(
                                    id={"type": "w8-note", "index": publication_id},
                                    value=note,
                                    placeholder="Add a short reading note",
                                    className="form-control small",
                                    style={"height": "60px"},
                                ),
                                xs=12,
                                md=8,
                                className="mt-2",
                            ),
                        ],
                        className="g-2",
                    ),
                    dbc.Button(
                        "Save Note",
                        id={"type": "w8-update-pub", "index": publication_id},
                        color="secondary",
                        size="sm",
                        className="mt-2",
                        n_clicks=0,
                    ),
                ],
                className="small border-bottom py-3",
            )
        )
    return html.Div(
        [
            html.P(
                f"Favorite Publications ({len(favorite_rows)})",
                className="small fw-semibold mb-1",
            ),
            html.Ul(favorite_items, className="list-unstyled mb-0 small"),
        ]
    )


def get_widget08_initial_favorites():
    return build_widget08_favorites_list(list_favorite_publications())



# define a function to builds the layout of Widget 08 in the dashboard
# the column for widget 08 is about the related keywors
def build_column_widget08():
    return dbc.Col(
        children=[
            html.Div(
                className="section-label-row",
                children=[
                    html.Span(
                        "SAVE & EDIT PUBLICATIONS",
                        className="section-label section-label-keyword",
                    )
                ],
            ),
            html.Div(
                className="widget-card accent-orange",
                children=[
                    html.Div(
                        className="widget-title-row",
                        children=[
                            html.Span("W8", className="widget-tag"),
                            html.Span(
                                "Favorite Publication Manager",
                                className="widget-title",
                            ),
                            html.Span("MongoDB", className="tech-badge mongo"),
                            html.Span("Insert/Delete/Modify", className="tech-badge transaction"),
                        ],
                    ),
                    html.P(
                        "Search papers, save favorites, and track reading notes.",
                        className="widget-subtitle",
                    ),
                    html.P(
                        "Examples: graph neural networks, information retrieval...",
                        className="text-muted small mb-2",
                    ),
                    html.Label(
                        className="widget-search-inline search-row-focus w8-search-row",
                        children=[
                            dcc.Input(
                                id="search_widget08",
                                type="text",
                                placeholder="Enter title or keyword to search",
                                size="72",
                                className="form-control",
                                debounce=True,
                                style={
                                    "minWidth": "0",
                                    "boxSizing": "border-box",
                                },
                            ),
                            dbc.Button(
                                "Search",
                                id="search_widget08_button",
                                color="secondary",
                                size="sm",
                                className="button-search-accent-orange",
                                n_clicks=0,
                            ),
                        ],
                    ),
                    html.Div(
                        id="widget_08_search_results",
                        className="mb-2",
                        children=get_widget08_initial_results_children(),
                    ),
                    html.Hr(className="my-2"),
                    html.Div(
                        id="widget_08_favorites",
                        children=get_widget08_initial_favorites(),
                    ),
                ],
            ),
        ],
        xs=12,
        sm=12,
        md=6,
        className="py-2",
    )
