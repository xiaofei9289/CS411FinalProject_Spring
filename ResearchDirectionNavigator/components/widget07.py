from dash import html, dcc
import dash_bootstrap_components as dbc
import math
import plotly.graph_objects as go

from utils.common import neo4j_faculty_id_to_mysql_id


def get_widget07_initial_results_children():
    return [
        html.P(
            "Type a faculty name to view their top coauthor network.",
            className="text-muted small mb-0",
        ),
    ]


def build_widget07_network_results(network_payload):
    center=network_payload.get("center")
    collaborators=network_payload.get("collaborators") or []
    if not center:
        return html.P(
            "No faculty matched that name in Neo4j.",
            className="text-muted small mb-0",
        )
    if not collaborators:
        return html.P(
            "This faculty was found, but no coauthor relationships were returned.",
            className="text-muted small mb-0",
        )
    graph_component=build_collaboration_network_graph(center, collaborators)
    collaborator_items=[]
    for collaborator in collaborators:
        mysql_faculty_id=neo4j_faculty_id_to_mysql_id(collaborator.get("faculty_id"))
        name=collaborator.get("faculty_name") or collaborator.get("faculty_id")
        if mysql_faculty_id is not None:
            name_component=dbc.Button(
                name,
                id={"type": "w4-open-faculty", "index": mysql_faculty_id},
                color="link",
                className="p-0 text-start small fw-semibold",
                n_clicks=0,
            )
        else:
            name_component=html.Span(name, className="small fw-semibold")
        collaborator_items.append(
            html.Li(
                [
                    name_component,
                    html.Span(
                        f" · {collaborator.get('shared_publications', 0)} shared publications",
                        className="text-muted small",
                    ),
                ],
                className="border-bottom py-1",
            )
        )
    return html.Div(
        [
            graph_component,
            html.P("Top collaborators", className="small fw-semibold mb-1"),
            html.Ul(collaborator_items, className="list-unstyled mb-0"),
        ]
    )


def build_collaboration_network_graph(center, collaborators):
    node_x=[0]
    node_y=[0]
    node_text=[center.get("faculty_name") or "Selected faculty"]
    node_size=[34]
    node_color=["#8659D7"]
    edge_x=[]
    edge_y=[]
    edge_text_x=[]
    edge_text_y=[]
    edge_text=[]
    count=len(collaborators)
    max_shared=max([int(row.get("shared_publications") or 0) for row in collaborators] or [1])
    for index, collaborator in enumerate(collaborators):
        angle=2*math.pi*index/max(count, 1)
        radius=1.0
        x=radius*math.cos(angle)
        y=radius*math.sin(angle)
        shared=int(collaborator.get("shared_publications") or 0)
        node_x.append(x)
        node_y.append(y)
        node_text.append(collaborator.get("faculty_name") or collaborator.get("faculty_id"))
        node_size.append(18+18*(shared/max(max_shared, 1)))
        node_color.append("#D8C6FF")
        edge_x.extend([0, x, None])
        edge_y.extend([0, y, None])
        edge_text_x.append(x/2)
        edge_text_y.append(y/2)
        edge_text.append(str(shared))
    edge_trace=go.Scatter(
        x=edge_x,
        y=edge_y,
        mode="lines",
        line=dict(width=2, color="rgba(90, 62, 160, 0.35)"),
        hoverinfo="none",
    )
    node_trace=go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text",
        text=node_text,
        textposition="bottom center",
        marker=dict(size=node_size, color=node_color, line=dict(width=1, color="#5A3EA0")),
        hoverinfo="text",
    )
    label_trace=go.Scatter(
        x=edge_text_x,
        y=edge_text_y,
        mode="text",
        text=edge_text,
        textfont=dict(size=11, color="#5A3EA0"),
        hoverinfo="none",
    )
    figure=go.Figure(data=[edge_trace, node_trace, label_trace])
    figure.update_layout(
        title=dict(text="Neo4j Coauthor Network", font=dict(color="#2C516E", size=16)),
        paper_bgcolor="#f5f6f8",
        plot_bgcolor="#f5f6f8",
        showlegend=False,
        margin=dict(l=10, r=10, t=45, b=10),
        height=360,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    )
    return dcc.Graph(figure=figure, config={"displayModeBar": False}, className="mb-2")



# W7 column layout
def build_column_widget07():
    return dbc.Col(
        children=[
            html.Div(
                className="section-label-row",
                children=[
                    html.Span(
                        "NETWORK & PERSONALIZATION",
                        className="section-label section-label-purple",
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
                        "Examples: Yann Lecun, Honglak...",
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
