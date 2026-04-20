"""Widget 8 — related keywords explorer (shell). Teammate implements Neo4j keyword grid/table in results."""

from dash import html, dcc
import dash_bootstrap_components as dbc


def get_widget08_initial_results_children():
    """Teammate: return keyword grid or table after Neo4j queries."""
    return [
        html.P(
            "Results area — teammate will render the related-keywords table here.",
            className="text-muted small mb-0",
        ),
    ]

# the column for widget 08 is about the related keywors
def build_column_widget08():
    """W8 column shell: same ids as before so layout and future callbacks stay valid."""
    return dbc.Col(
        children=[
            html.Div(
                className="section-label-row",
                children=[
                    html.Span(
                        "RELATED KEYWORDS EXPLORATION",
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
                                "Related Keywords Explorer",
                                className="widget-title",
                            ),
                            html.Span("Neo4j", className="tech-badge neo4j"),
                        ],
                    ),
                    html.P(
                        "Discover related research keywords and connections.",
                        className="widget-subtitle",
                    ),
                    html.P(
                        "Examples: computer science, databases...",
                        className="text-muted small mb-2",
                    ),
                    html.Label(
                        className="widget-search-inline search-row-focus w8-search-row",
                        children=[
                            dcc.Input(
                                id="search_widget08",
                                type="text",
                                placeholder="Enter keywords to search",
                                size="72",
                                className="form-control",
                                debounce=True,
                                style={
                                    "minWidth": "0",
                                    "boxSizing": "border-box",
                                },
                            ),
                            dbc.Button(
                                "Explore",
                                id="search_widget08_button",
                                color="secondary",
                                size="sm",
                                className="button-search-accent-orange",
                                n_clicks=0,
                            ),
                        ],
                    ),
                    html.Div(
                        id="widget_08_results",
                        children=get_widget08_initial_results_children(),
                    ),
                ],
            ),
        ],
        xs=12,
        sm=12,
        md=6,
        className="py-2",
    )
