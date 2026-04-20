from dash import html, dcc
import dash_bootstrap_components as dbc


def get_widget06_initial_results_children():
    """TODO: replace this placeholder after W6 recommendation callbacks are implemented."""
    return [
        html.P(
            "TODO: W6 smart faculty recommendation is not implemented yet.",
            className="text-muted small mb-0",
        ),
    ]

# TODO: implement W6 callbacks and data access for ranked faculty recommendations.



# define a function to builds the layout of Widget 06 in the dashboard
# the column for widget 06 is about the smart recommendation
def build_column_widget06():
    """W6 column shell: same ids as before so layout and future callbacks stay valid."""
    return dbc.Col(
        children=[
            html.Div(
                className="section-label-row",
                children=[
                    html.Span(
                        "CORE DISCOVERY",
                        className="section-label section-label-core",
                    )
                ],
            ),
            html.Div(
                className="widget-card accent-green",
                children=[
                    html.Div(
                        className="widget-title-row",
                        children=[
                            html.Span("W6", className="widget-tag"),
                            html.Span(
                                "Smart Faculty Recommendation",
                                className="widget-title",
                            ),
                            html.Span("Neo4j", className="tech-badge neo4j"),
                            html.Span("MySQL", className="tech-badge mysql"),
                            html.Span("MongoDB", className="tech-badge mongo"),
                            html.Span("⭐ Highlight", className="tech-badge highlight"),
                        ],
                    ),
                    html.P(
                        "Find promising professors based on topic relevance, "
                        "publication volume, and recent activity.",
                        className="widget-subtitle",
                    ),
                    html.P(
                        "Examples: deep learning, cybersecurity, bioinformatics...",
                        className="text-muted small mb-2",
                    ),
                    html.Label(
                        className="widget-search-inline search-row-focus",
                        children=[
                            dcc.Input(
                                id="search_widget06",
                                type="text",
                                placeholder="Enter topics to search",
                                className="form-control",
                                debounce=True,
                            ),
                            dbc.Button(
                                "Recommend",
                                id="search_widget06_button",
                                color="secondary",
                                size="sm",
                                className="button-search-accent-green",
                                n_clicks=0,
                            ),
                        ],
                    ),
                    html.Div(
                        id="widget_06_results",
                        children=get_widget06_initial_results_children(),
                    ),
                ],
            ),
        ],
        xs=12,
        sm=12,
        md=7,
        className="py-2",
    )
