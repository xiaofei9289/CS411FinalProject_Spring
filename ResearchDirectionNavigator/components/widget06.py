from dash import html, dcc
import dash_bootstrap_components as dbc


def get_widget06_initial_results_children():
    return [
        html.P(
            "Type a topic and tune the weights to rank faculty recommendations.",
            className="text-muted small mb-0",
        ),
    ]


def build_widget06_recommendation_results(recommendation_payload):
    rows=recommendation_payload.get("rows") or []
    message=recommendation_payload.get("message") or ""
    if not rows:
        return html.P(message or "No recommendations found.", className="text-muted small mb-0")
    table_rows=[]
    for rank, row in enumerate(rows, start=1):
        faculty_id=int(row["faculty_id"])
        faculty_name_button=dbc.Button(
            row.get("faculty_name") or f"Faculty {faculty_id}",
            id={"type": "w4-open-faculty", "index": faculty_id},
            color="link",
            className="p-0 text-start fw-semibold small",
            n_clicks=0,
        )
        table_rows.append(
            html.Tr(
                [
                    html.Td(str(rank)),
                    html.Td(
                        [
                            faculty_name_button,
                            html.Div(row.get("university_name") or "", className="text-muted small"),
                        ]
                    ),
                    html.Td(str(row.get("graph_relevance") or 0)),
                    html.Td(f"{row.get('keyword_relevant_citations', 0)}"),
                    html.Td(str(row.get("recent_publication_count") or 0)),
                    html.Td(f"{row.get('score', 0)}"),
                ]
            )
        )
    topic=recommendation_payload.get("topic") or "your topic"
    topic_activity_total=recommendation_payload.get("topic_activity_total") or 0
    return html.Div(
        [
            html.P(
                f'MongoDB found {topic_activity_total} publication-year matches for "{topic}" as topic activity context.',
                className="small text-muted mb-2",
            ),
            dbc.Table(
                [
                    html.Thead(
                        html.Tr(
                            [
                                html.Th("#"),
                                html.Th("Faculty"),
                                html.Th("Neo4j relevance"),
                                html.Th("K-citations"),
                                html.Th("Recent"),
                                html.Th("Score"),
                            ]
                        )
                    ),
                    html.Tbody(table_rows),
                ],
                bordered=True,
                hover=True,
                responsive=True,
                size="sm",
                className="mb-0 align-middle",
            ),
        ]
    )



# W6 column layout
def build_column_widget06():
    # W6 layout
    return dbc.Col(
        children=[
            html.Div(
                className="section-label-row",
                children=[
                    html.Span(
                        "CORE DISCOVERY",
                        className="section-label section-label-green",
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
                        "keyword-relevant citations, and recent activity.",
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
                        [
                            html.Label("Neo4j topic weight", className="small fw-semibold"),
                            dcc.Slider(
                                id="widget06_graph_weight",
                                min=0,
                                max=1,
                                step=0.1,
                                value=0.5,
                                marks=None,
                                tooltip={"placement": "bottom", "always_visible": False},
                            ),
                            html.Label("Keyword-relevant citation weight", className="small fw-semibold mt-2"),
                            dcc.Slider(
                                id="widget06_citation_weight",
                                min=0,
                                max=1,
                                step=0.1,
                                value=0.3,
                                marks=None,
                                tooltip={"placement": "bottom", "always_visible": False},
                            ),
                            html.Label("Recent activity weight", className="small fw-semibold mt-2"),
                            dcc.Slider(
                                id="widget06_recent_weight",
                                min=0,
                                max=1,
                                step=0.1,
                                value=0.2,
                                marks=None,
                                tooltip={"placement": "bottom", "always_visible": False},
                            ),
                        ],
                        className="mb-3",
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
