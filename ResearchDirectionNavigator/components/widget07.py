"""Widget 7 — collaboration network (shell). Teammate implements Neo4j graph / table in results."""

from dash import html, dcc
import dash_bootstrap_components as dbc


def get_widget07_initial_results_children():
    """Teammate: return graph or table after Neo4j queries."""
    return [
        html.P(
            "Results area — teammate will render the collaboration network here.",
            className="text-muted small mb-0",
        ),
    ]

# the column for widget 07 is about the collaboration network
def build_column_widget07():
    return dbc.Col(
        children=[
            html.Div(
                className="section-label-row",
                children=[
                    html.Span(
                        "NETWORK & PERSONALIZATION",
                        className="section-label section-label-network",
                    )
                ],
            ),
            html.Div(
                className="widget-card accent-purple",
                children=[
                    html.Div(
                        className="widget-title-row",
                        children=[
                            html.Span("W7", className="widget-tag"),
                            html.Span(
                                "Collaboration Network",
                                className="widget-title",
                            ),
                            html.Span("Neo4j", className="tech-badge neo4j"),
                        ],
                    ),
                    html.P(
                        "Explore collaboration relationships between faculty.",
                        className="widget-subtitle",
                    ),
                    html.P(
                        "Examples: Jane Smith, Wei Zhang, Maria Garcia...",
                        className="text-muted small mb-2",
                    ),
                    html.Label(
                        className="widget-search-inline search-row-focus",
                        children=[
                            dcc.Input(
                                id="search_widget07",
                                type="text",
                                placeholder="Enter faculty name to search",
                                className="form-control",
                                debounce=True,
                            ),
                            dbc.Button(
                                "Show Network",
                                id="search_widget07_button",
                                color="secondary",
                                size="sm",
                                className="button-search-accent-purple",
                                n_clicks=0,
                            ),
                        ],
                    ),
                    html.Div(
                        id="widget_07_results",
                        children=get_widget07_initial_results_children(),
                    ),
                ],
            ),
        ],
        xs=12,
        sm=12,
        md=4,
        className="py-2",
    )
